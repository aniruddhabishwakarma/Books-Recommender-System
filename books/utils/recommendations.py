import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from books.models.user_model import FavoriteBook
from books.models.books_model import Book
import random


def get_recommended_books(user, num_recommendations=5):
    """Generates book recommendations based on one randomly selected favorite book."""

    user_favorites = FavoriteBook.objects.filter(user=user).select_related("book")
    if not user_favorites.exists():
        return None, []  # No favorite book, return empty recommendations

    # Select one random favorite book if user has multiple
    selected_favorite = random.choice(user_favorites)

    # Get the favorite book's ID and description
    favorite_book_id = selected_favorite.book.id
    favorite_description = selected_favorite.book.description

    # Get all books excluding the selected favorite
    all_books = Book.objects.exclude(id=favorite_book_id)
    if not all_books.exists():
        return selected_favorite.book.title, []  # Return favorite book title with no recommendations

    # Prepare book data
    all_books_data = list(all_books.values_list("id", "title", "categories", "description"))
    book_ids = [b[0] for b in all_books_data]
    book_texts = [f"{b[1]} {b[2]} {b[3]}" for b in all_books_data]  # Combine title, category, and description

    # Apply TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    book_vectors = tfidf_vectorizer.fit_transform(book_texts)  # Transform all books
    favorite_vector = tfidf_vectorizer.transform([favorite_description])  # Transform the favorite book

    # Compute Cosine Similarity
    similarity_scores = cosine_similarity(favorite_vector, book_vectors)[0]

    # Get top recommendations
    similar_indices = np.argsort(-similarity_scores)[:num_recommendations]  # Get top `num_recommendations`
    recommended_books = [all_books.get(id=book_ids[i]) for i in similar_indices if i < len(book_ids)]

    return selected_favorite.book.title, recommended_books  # Return favorite book title and recommendations

def get_combined_recommendations(user, total_recommendations=15):
    """Recommends books for all favorites, ensuring 15 total recommendations in a randomized manner."""

    user_favorites = FavoriteBook.objects.filter(user=user).select_related("book")
    if not user_favorites.exists():
        return []  # No recommendations if user has no favorites

    favorite_books = list(user_favorites)
    num_favorites = len(favorite_books)

    # Adjust the number of recommendations per favorite book
    if num_favorites == 1:
        recommendations_per_fav = [15]
    elif num_favorites == 2:
        recommendations_per_fav = [7, 8]  # Distribute approximately
    else:
        recommendations_per_fav = [5] * min(num_favorites, 3)  # Distribute evenly for up to 3 favorites

    # Get all books excluding user's favorites
    all_books = Book.objects.exclude(id__in=[fav.book.id for fav in favorite_books])
    if not all_books.exists():
        return []

    # Prepare book data
    all_books_data = list(all_books.values_list("id", "title", "categories", "description"))
    book_ids = [b[0] for b in all_books_data]
    book_texts = [f"{b[1]} {b[2]} {b[3]}" for b in all_books_data]  # Combine title, category, and description

    # Apply TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    book_vectors = tfidf_vectorizer.fit_transform(book_texts)  # Transform all books

    combined_recommendations = []  # Store recommendations

    for idx, fav in enumerate(favorite_books[:3]):  # Consider only up to 3 favorites
        if fav.book.description:
            favorite_vector = tfidf_vectorizer.transform([fav.book.description])  # Transform the favorite book
            similarity_scores = cosine_similarity(favorite_vector, book_vectors)[0]

            # Get top recommendations for this favorite
            num_recommendations = recommendations_per_fav[idx]
            similar_indices = np.argsort(-similarity_scores)[:num_recommendations]  # Get top books
            similar_books = [all_books.get(id=book_ids[i]) for i in similar_indices if i < len(book_ids)]

            combined_recommendations.extend(similar_books)  # Add to list

    # Shuffle recommendations for randomness
    random.shuffle(combined_recommendations)

    return combined_recommendations[:total_recommendations]  # Ensure exactly 15 books


def get_book_similarity_matrix(books):
    """Generates a similarity matrix for books based on their descriptions and categories."""
    if not books:
        return None, []

    book_ids = [book.id for book in books]
    book_texts = [f"{book.title} {book.categories} {book.description}" for book in books]

    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    book_vectors = tfidf_vectorizer.fit_transform(book_texts)

    similarity_matrix = cosine_similarity(book_vectors)
    
    return similarity_matrix, book_ids


def get_similar_books(book, all_books, similarity_matrix, book_ids, num_similar=3):
    """Finds top `num_similar` similar books based on content similarity."""
    try:
        book_index = book_ids.index(book.id)
    except ValueError:
        return []

    # Get top `num_similar` similar books
    similar_indices = np.argsort(-similarity_matrix[book_index])[: num_similar + 1]  # +1 to exclude itself
    similar_books = [all_books[i] for i in similar_indices if all_books[i].id != book.id]

    return similar_books[:num_similar]


def get_similar_users_recommendations(user, num_recommendations=5, num_similar=3):
    """Finds books liked by similar users and also recommends similar books for each one."""
    
    # Get the current user's favorite books
    user_favorites = set(FavoriteBook.objects.filter(user=user).values_list("book_id", flat=True))

    if not user_favorites:
        return []  # No recommendations if the user has no favorites

    # Find users who liked the same books
    similar_users = set(FavoriteBook.objects.filter(book_id__in=user_favorites)
                        .exclude(user=user)
                        .values_list("user", flat=True))

    if not similar_users:
        return []  # No similar users found

    # Get books favorited by similar users (excluding books the user already liked)
    recommended_book_ids = set(FavoriteBook.objects
                               .filter(user_id__in=similar_users)
                               .exclude(book_id__in=user_favorites)
                               .values_list("book_id", flat=True))

    # Fetch book details
    recommended_books = list(Book.objects.filter(id__in=recommended_book_ids))

    if not recommended_books:
        return []

    # Compute similarity matrix for all books
    similarity_matrix, book_ids = get_book_similarity_matrix(recommended_books)

    # Use a set to track unique recommended books
    unique_books_with_similars = set()

    # Get similar books for each recommended book
    books_with_similars = []
    for book in recommended_books:
        similar_books = get_similar_books(book, recommended_books, similarity_matrix, book_ids, num_similar=num_similar)

        # Ensure books are unique
        if book.id not in unique_books_with_similars:
            unique_books_with_similars.add(book.id)
            books_with_similars.append({"book": book, "similar_books": similar_books})

    # Shuffle books for diversity
    random.shuffle(books_with_similars)

    return books_with_similars[:num_recommendations]  # Return limited recommendations