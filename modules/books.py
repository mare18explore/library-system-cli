from db import connect
from datetime import datetime

def search_books(keyword):
    """
    Returns a list of books that match a title or author keyword.
    Also includes average rating and availability status.
    """
    conn, cur = connect()
    cur.execute("""
        SELECT b.book_id, b.title, b.author, b.pyear,
               IFNULL(ROUND(AVG(r.rating), 1), 'NA') as avg_rating,
               CASE
                   WHEN EXISTS (
                       SELECT 1 FROM borrowings br 
                       WHERE br.book_id = b.book_id AND br.end_date IS NULL
                   ) THEN 'Not Available'
                   ELSE 'Available'
               END as availability
        FROM books b
        LEFT JOIN reviews r ON r.book_id = b.book_id
        WHERE b.title LIKE ? OR b.author LIKE ?
        GROUP BY b.book_id
        ORDER BY b.title
    """, (f"%{keyword}%", f"%{keyword}%"))
    return cur.fetchall()


def borrow_book(book_id, email):
    """
    Allows a user to borrow a book if it's available.
    Returns True if borrowed successfully, False if already borrowed.
    """
    conn, cur = connect()
    
    # Check if book is already borrowed
    cur.execute("SELECT 1 FROM borrowings WHERE book_id = ? AND end_date IS NULL", (book_id,))
    if cur.fetchone():
        return False  # Book already borrowed

    # Get next available bid
    cur.execute("SELECT MAX(bid) FROM borrowings")
    max_bid = cur.fetchone()[0]
    new_bid = (max_bid or 0) + 1

    cur.execute("""
        INSERT INTO borrowings (bid, member, book_id, start_date)
        VALUES (?, ?, ?, DATE('now'))
    """, (new_bid, email, book_id))
    
    conn.commit()
    return True


def return_book(bid, email):
    """
    Handles book return and checks if a penalty is needed.
    Returns number of late days if overdue, or 0 if returned on time.
    Returns None if invalid return (e.g., wrong user or already returned).
    """
    conn, cur = connect()
    
    # Check if this borrowing exists and is active
    cur.execute("""
        SELECT start_date FROM borrowings 
        WHERE bid = ? AND member = ? AND end_date IS NULL
    """, (bid, email))
    row = cur.fetchone()
    
    if not row:
        return None  # Invalid return (either already returned or wrong user)
    
    # Mark the book as returned
    cur.execute("UPDATE borrowings SET end_date = DATE('now') WHERE bid = ?", (bid,))
    conn.commit()

    # Calculate penalty (if overdue)
    start_date = datetime.strptime(row["start_date"], "%Y-%m-%d")
    due_date = start_date.replace(day=start_date.day + 20)
    today = datetime.today()
    late_days = (today - due_date).days
    
    return late_days if late_days > 0 else 0