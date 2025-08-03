from db import connect
from db import get_connection
from colorama import Fore
from datetime import datetime

def get_active_borrowings(email):
    """
    Returns a list of active (not returned) borrowings for the given user.
    Each item includes the borrowing ID, book title, and borrow date.
    """
    conn, cur = connect()
    
    cur.execute("""
        SELECT b.bid, bk.title, b.start_date
        FROM borrowings b
        JOIN books bk ON b.book_id = bk.book_id
        WHERE b.member = ? AND b.end_date IS NULL
    """, (email,))
    
    borrowings = cur.fetchall()
    conn.close()
    return borrowings

# Show general library stats in the CLI
def show_library_stats():
    con = get_connection()
    cur = con.cursor()

    # Most borrowed books overall (top 3)
    print(Fore.MAGENTA + "\nTop 3 Most Borrowed Books:")
    cur.execute("""
        SELECT books.title, COUNT(*) as borrow_count
        FROM borrowings
        JOIN books ON borrowings.book_id = books.book_id
        GROUP BY books.book_id
        ORDER BY borrow_count DESC
        LIMIT 3
    """)
    rows = cur.fetchall()
    for title, count in rows:
        print(f" - {title} ({count} times)")

    # Members with the most borrowings
    print(Fore.MAGENTA + "\nMost Active Members:")
    cur.execute("""
        SELECT members.name, COUNT(*) as borrow_count
        FROM borrowings
        JOIN members ON borrowings.member = members.email
        GROUP BY members.email
        ORDER BY borrow_count DESC
        LIMIT 3
    """)
    rows = cur.fetchall()
    for name, count in rows:
        print(f" - {name} ({count} borrowings)")

    # Books with highest average ratings (min 2 reviews)
    print(Fore.MAGENTA + "\nHighest Rated Books (at least 2 reviews):")
    cur.execute("""
        SELECT books.title, ROUND(AVG(reviews.rating), 1) as avg_rating
        FROM reviews
        JOIN books ON reviews.book_id = books.book_id
        GROUP BY books.book_id
        HAVING COUNT(reviews.rating) >= 2
        ORDER BY avg_rating DESC
        LIMIT 3
    """)
    rows = cur.fetchall()
    for title, rating in rows:
        print(f" - {title} ({rating} average rating)")

    # Total books borrowed in the current month
    print(Fore.MAGENTA + "\nBorrowing Activity This Month:")
    cur.execute("""
        SELECT COUNT(*)
        FROM borrowings
        WHERE strftime('%Y-%m', start_date) = strftime('%Y-%m', 'now')
    """)
    total = cur.fetchone()[0]
    current_month = datetime.today().strftime('%B %Y')
    print(f" - {total} books borrowed in {current_month}")

    con.close()