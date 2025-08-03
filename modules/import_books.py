from db import get_connection
import requests
from colorama import Fore

def fetch_books_from_api(keyword="python"):
    """
    Fetches books from Open Library API based on a keyword.
    Returns a list of tuples: (title, author, year)
    """
    try:
        url = f"https://openlibrary.org/search.json?q={keyword}&limit=10"
        response = requests.get(url)
        response.raise_for_status()  # Raise error if API call fails

        data = response.json()

        books = []
        for item in data.get("docs", []):
            title = item.get("title", "Unknown Title").strip()
            authors = [a.strip() for a in item.get("author_name", ["Unknown Author"])]
            year = item.get("first_publish_year", 0)

            # Join multiple authors into one string
            author_str = ", ".join(authors)
            books.append((title, author_str, year))

        return books

    except Exception as e:
        print(Fore.RED + f"[Error fetching books]: {e}")
        return []

def insert_books_into_db(books):
    """
    Inserts books into the DB if the title does not already exist.
    Skips duplicates by checking existing titles first.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Get all existing book titles into a set for fast lookup
        cur.execute("SELECT title FROM books")
        existing_titles = set(row[0].lower() for row in cur.fetchall())

        # Get the current highest book_id
        cur.execute("SELECT MAX(book_id) FROM books")
        result = cur.fetchone()
        start_id = result[0] + 1 if result[0] else 1

        inserted_count = 0
        # skip duplicate title
        for i, (title, author, year) in enumerate(books):
            if title.lower() in existing_titles:
                continue  

            cur.execute("""
                INSERT INTO books (book_id, title, author, pyear)
                VALUES (?, ?, ?, ?)
            """, (start_id + inserted_count, title, author, year))
            inserted_count += 1

        conn.commit()
        print(f"[Success] {inserted_count} new books inserted (skipped duplicates).")
    except Exception as e:
        print(f"[DB Insert Error]: {e}")
    finally:
        if conn:
            conn.close()

def main():
    print(Fore.CYAN + "=== Import Books from Open Library API ===")
    keyword = input("Enter a keyword (e.g. 'fantasy', 'history', 'mystery'): ").strip()
    if not keyword:
        print("No keyword entered. Aborting.")
        return

    books = fetch_books_from_api(keyword)
    if not books:
        print("No books found or API failed.")
        return

    insert_books_into_db(books)


if __name__ == "__main__":
    main()