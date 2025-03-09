import requests
import time
import random
import pandas as pd

# ✅ Google Books API Base URL
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# ✅ Categories we want to fetch
SELECTED_CATEGORIES = [
    "Education", "Social Science", "Philosophy", "Fiction", "Computers",
    "History", "Humor", "Political science", "Beauty culture",
    "Current Events", "Psychology", "Religion", "Performing Arts",
    "Cooking", "Biography & Autobiography", "Business & Economics",
    "Health & Fitness"
]

# ✅ Fetch 300 books per category with delay
BOOKS_PER_CATEGORY = 300
BOOKS_PER_REQUEST = 40
PAGES_PER_CATEGORY = BOOKS_PER_CATEGORY // BOOKS_PER_REQUEST

def fetch_books_by_category(category):
    """Fetch books from Google Books API with random delay to prevent rate limits."""
    books = []
    start_index = 0

    for page in range(PAGES_PER_CATEGORY):
        try:
            params = {
                "q": f"subject:{category}",
                "maxResults": BOOKS_PER_REQUEST,
                "startIndex": start_index,
                "printType": "books",
                "projection": "full",
            }
            response = requests.get(GOOGLE_BOOKS_API_URL, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                new_books = data.get("items", [])

                if not new_books:
                    print(f"✔️ No more books found for {category}. Stopping pagination.")
                    break

                books.extend(new_books)
                start_index += BOOKS_PER_REQUEST
                print(f"📚 Fetched {len(books)} books so far for {category}...")

                # ✅ Random delay to avoid blocking (1 to 5 seconds)
                time.sleep(random.uniform(1, 5))

            else:
                print(f"❌ Failed to fetch books for {category} (Page {page}). Status: {response.status_code}")
                break

        except requests.exceptions.ConnectionError:
            print("🚨 Connection error! Waiting 10 seconds before retrying...")
            time.sleep(10)
        except requests.exceptions.Timeout:
            print("⏳ Request timed out. Retrying after 5 seconds...")
            time.sleep(5)

    return books

# ✅ Fetch books for all selected categories
all_books = []
for category in SELECTED_CATEGORIES:
    print(f"📚 Fetching 300 books for category: {category}...")
    books = fetch_books_by_category(category)
    
    for book in books:
        volume_info = book.get("volumeInfo", {})
        sale_info = book.get("saleInfo", {})

        image_links = volume_info.get("imageLinks", {})
        high_res_image = (
            image_links.get("extraLarge") or 
            image_links.get("large") or 
            image_links.get("medium") or 
            image_links.get("thumbnail") or 
            image_links.get("smallThumbnail", "")
        )

        book_data = {
            "id": book.get("id", ""),
            "title": volume_info.get("title", "Unknown Title"),
            "authors": ", ".join(volume_info.get("authors", ["Unknown"])),
            "categories": category,
            "published_date": volume_info.get("publishedDate", ""),
            "publisher": volume_info.get("publisher", "Unknown"),
            "description": volume_info.get("description", ""),
            "price": sale_info.get("listPrice", {}).get("amount", "Not Available"),
            "currency": sale_info.get("listPrice", {}).get("currencyCode", ""),
            "thumbnail": high_res_image,
            "info_link": volume_info.get("infoLink", ""),
        }
        all_books.append(book_data)

# ✅ Save to CSV
df = pd.DataFrame(all_books)
df.to_csv("google_books_300_per_category.csv", index=False)
print(f"✅ Successfully saved {len(all_books)} books to CSV!")
import requests
import time
import random
import pandas as pd

# ✅ Google Books API Base URL
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# ✅ Categories we want to fetch
SELECTED_CATEGORIES = [
    "Education", "Social Science", "Philosophy", "Fiction", "Computers",
    "History", "Humor", "Political science", "Beauty culture",
    "Current Events", "Psychology", "Religion", "Performing Arts",
    "Cooking", "Biography & Autobiography", "Business & Economics",
    "Health & Fitness"
]

# ✅ Fetch 300 books per category with delay
BOOKS_PER_CATEGORY = 300
BOOKS_PER_REQUEST = 40
PAGES_PER_CATEGORY = BOOKS_PER_CATEGORY // BOOKS_PER_REQUEST

def fetch_books_by_category(category):
    """Fetch books from Google Books API with random delay to prevent rate limits."""
    books = []
    start_index = 0

    for page in range(PAGES_PER_CATEGORY):
        try:
            params = {
                "q": f"subject:{category}",
                "maxResults": BOOKS_PER_REQUEST,
                "startIndex": start_index,
                "printType": "books",
                "projection": "full",
            }
            response = requests.get(GOOGLE_BOOKS_API_URL, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                new_books = data.get("items", [])

                if not new_books:
                    print(f"✔️ No more books found for {category}. Stopping pagination.")
                    break

                books.extend(new_books)
                start_index += BOOKS_PER_REQUEST
                print(f"📚 Fetched {len(books)} books so far for {category}...")

                # ✅ Random delay to avoid blocking (1 to 5 seconds)
                time.sleep(random.uniform(1, 5))

            else:
                print(f"❌ Failed to fetch books for {category} (Page {page}). Status: {response.status_code}")
                break

        except requests.exceptions.ConnectionError:
            print("🚨 Connection error! Waiting 10 seconds before retrying...")
            time.sleep(10)
        except requests.exceptions.Timeout:
            print("⏳ Request timed out. Retrying after 5 seconds...")
            time.sleep(5)

    return books

# ✅ Fetch books for all selected categories
all_books = []
for category in SELECTED_CATEGORIES:
    print(f"📚 Fetching 300 books for category: {category}...")
    books = fetch_books_by_category(category)
    
    for book in books:
        volume_info = book.get("volumeInfo", {})
        sale_info = book.get("saleInfo", {})

        image_links = volume_info.get("imageLinks", {})
        high_res_image = (
            image_links.get("extraLarge") or 
            image_links.get("large") or 
            image_links.get("medium") or 
            image_links.get("thumbnail") or 
            image_links.get("smallThumbnail", "")
        )

        book_data = {
            "id": book.get("id", ""),
            "title": volume_info.get("title", "Unknown Title"),
            "authors": ", ".join(volume_info.get("authors", ["Unknown"])),
            "categories": category,
            "published_date": volume_info.get("publishedDate", ""),
            "publisher": volume_info.get("publisher", "Unknown"),
            "description": volume_info.get("description", ""),
            "price": sale_info.get("listPrice", {}).get("amount", "Not Available"),
            "currency": sale_info.get("listPrice", {}).get("currencyCode", ""),
            "thumbnail": high_res_image,
            "info_link": volume_info.get("infoLink", ""),
        }
        all_books.append(book_data)

# ✅ Save to CSV
df = pd.DataFrame(all_books)
df.to_csv("google_books_300_per_category.csv", index=False)
print(f"✅ Successfully saved {len(all_books)} books to CSV!")
