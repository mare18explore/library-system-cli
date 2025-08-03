from db import connect
from utils.utils import is_valid_email, is_valid_name, is_valid_faculty
import bcrypt

def account_exists(email):
    """
    Checks if an account with the given email already exists in the DB.
    """
    con, cur = connect()
    cur.execute("SELECT email FROM members WHERE email = ?", (email,))
    result = cur.fetchone()
    con.close()
    return result is not None

def login_user(email, password):
    """
    Verifies user credentials. Returns True if match is found, else False.
    """
    try:
        con, cur = connect()
        cur.execute("SELECT passwd FROM members WHERE email = ?", (email,))
        row = cur.fetchone()
        con.close()

        if row:
            stored_hash = row["passwd"]
            # Convert to bytes if it's a string
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")

            if bcrypt.checkpw(password.encode(), stored_hash):
                return True
        return False
    except Exception as e:
        print("Error during login:", e)
        return False

def signup_user(email, password, name, byear, faculty):
    """
    Registers a new user account into the members table.
    Returns True if successful, False if error occurs (e.g., duplicate).
    """
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        conn, cur = connect()
        cur.execute("""
            INSERT INTO members (email, passwd, name, byear, faculty)
            VALUES (?, ?, ?, ?, ?)
        """, (email, hashed, name, byear, faculty))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Signup error: {e}")
        return False
    