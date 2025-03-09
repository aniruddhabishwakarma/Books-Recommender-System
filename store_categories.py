import os
import django
import pandas as pd

# ✅ Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_recommender.settings")
django.setup()

from books.models.books_model import Book

# Load CSV file
csv_file = "google_books_300_per_category.csv"
df = pd.read_csv(csv_file)

df.fillna("", inplace=True)  # Handle missing values

# ✅ Store books in the database
for _, row in df.iterrows():
    # Convert price to decimal, or set to None if not available
    try:
        price = float(row["price"]) if row["price"] != "Not Available" else None
    except ValueError:
        price = None

    if not Book.objects.filter(id=row["id"]).exists():
        Book.objects.create(
            id=row["id"],
            title=row["title"],
            authors=row["authors"],
            categories=row["categories"],
            published_date=row["published_date"],
            publisher=row["publisher"],
            description=row["description"],
            price=price,
            currency=row["currency"],
            thumbnail=row["thumbnail"],
            info_link=row["info_link"],
        )

print(f"✅ Successfully stored {len(df)} books in the database!")
