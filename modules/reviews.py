from db import connect
from datetime import date

def leave_review(email, bid, rating, review_text):
    """
    Saves a review and rating for the book associated with the given borrowing ID.
    - Gets book_id based on borrowing ID
    - Inserts a new review with user input
    """
    conn, cur = connect()

    # Get book_id from the borrowing record
    cur.execute("SELECT book_id FROM borrowings WHERE bid = ?", (bid,))
    result = cur.fetchone()

    if not result:
        print("Invalid borrowing ID.")
        return False
    
    book_id = result["book_id"]

    # Get next available review ID
    cur.execute("SELECT MAX(rid) FROM reviews")
    last_rid = cur.fetchone()[0]
    new_rid = (last_rid or 0) + 1

    # Insert the review
    try:
        cur.execute("""
            INSERT INTO reviews (rid, book_id, member, rating, rtext, rdate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (new_rid, book_id, email, rating, review_text, str(date.today())))
        conn.commit()
        return True
    except Exception as e:
        print(f"[Review Error] {e}")
        return False