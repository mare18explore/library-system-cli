from db import connect

def get_unpaid_penalties(email):
    """
    Returns a list of unpaid penalties for a given user.
    Each item includes: pid, amount due, amount paid so far.
    """
    conn, cur = connect()
    cur.execute("""
        SELECT p.pid, p.amount, IFNULL(p.paid_amount, 0) AS paid
        FROM penalties p
        JOIN borrowings b ON b.bid = p.bid
        WHERE b.member = ? AND (p.paid_amount IS NULL OR p.amount > p.paid_amount)
    """, (email,))
    return cur.fetchall()


def pay_penalty(pid, amount):
    """
    Adds payment amount to an existing penalty.
    """
    conn, cur = connect()
    cur.execute("""
        UPDATE penalties
        SET paid_amount = IFNULL(paid_amount, 0) + ?
        WHERE pid = ?
    """, (amount, pid))
    conn.commit()


def create_penalty(bid, late_days):
    """
    Creates a penalty for a borrowing entry if it was returned late.
    Each late day adds $1. Returns newly created penalty ID.
    """
    conn, cur = connect()

    # Get next penalty ID
    cur.execute("SELECT MAX(pid) FROM penalties")
    last_pid = cur.fetchone()[0]
    new_pid = (last_pid or 0) + 1

    cur.execute("""
        INSERT INTO penalties (pid, bid, amount, paid_amount)
        VALUES (?, ?, ?, 0)
    """, (new_pid, bid, late_days))

    conn.commit()
    return new_pid