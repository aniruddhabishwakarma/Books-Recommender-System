from django.shortcuts import render,get_object_or_404
import random
from books.models.books_model import Book
from books.models.user_model import FavoriteBook
from books.utils.recommendations import get_recommended_books, get_combined_recommendations, get_similar_users_recommendations

def home(request):
    """Home page with personalized recommendations, including similar users' books."""
    
    favorite_title, recommended_books = None, []
    top_recommendations = []
    similar_users_recommendations = []

    if request.user.is_authenticated:
        # Get 15 top recommendations shuffled from all favorites
        top_recommendations = get_combined_recommendations(request.user, total_recommendations=15)

        # Select one random favorite for "Because you liked"
        favorite_title, recommended_books = get_recommended_books(request.user, num_recommendations=5)

        # Get books liked by similar users + 3 similar books for each
        similar_users_recommendations = get_similar_users_recommendations(request.user, num_recommendations=5, num_similar=3)

        # Remove duplicate books from similar users' recommendations
        unique_books = set()
        filtered_similar_users_recommendations = []
        
        for item in similar_users_recommendations:
            if item["book"].id not in unique_books:
                unique_books.add(item["book"].id)
                filtered_similar_users_recommendations.append(item)

        similar_users_recommendations = filtered_similar_users_recommendations

    # If no recommendations, show 20 random books
    if not recommended_books and not top_recommendations and not similar_users_recommendations:
        books = list(Book.objects.all())
        random_books = random.sample(books, min(len(books), 20))
        return render(request, "home.html", {"books": random_books})

    return render(
        request, 
        "home.html", 
        {
            "top_recommendations": top_recommendations,
            "favorite_title": favorite_title,
            "recommended_books": recommended_books,
            "similar_users_recommendations": similar_users_recommendations,
        }
    )

def book_detail(request, book_id):
    """Displays details of a book and checks if it's in the user's favorites."""
    book = get_object_or_404(Book, id=book_id)

    # Check if the book is favorited by the logged-in user
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteBook.objects.filter(user=request.user, book=book).exists()

    return render(request, "book_detail.html", {"book": book, "is_favorited": is_favorited})

def search_books(request):
    """Search books by title or author."""
    query = request.GET.get("query", "").strip()
    books = Book.objects.filter(title__icontains=query) if query else []

    return render(request, "search_results.html", {"books": books, "query": query})

def books_by_category(request, category):
    """View to display books of a specific category."""
    books = Book.objects.filter(categories__icontains=category)  # Case-insensitive match
    categories = Book.objects.values_list("categories", flat=True).distinct()  # Get unique categories

    return render(request, "category_books.html", {"books": books, "category": category, "categories": categories})