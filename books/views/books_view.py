from django.shortcuts import render,get_object_or_404
import random
from books.models.books_model import Book
from books.models.user_model import FavoriteBook


def home(request):
    # Get 100 random books
    books = list(Book.objects.all())
    random_books = random.sample(books, min(len(books), 20))  # Handle case if less than 100 books

    return render(request, "home.html", {"books": random_books})

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