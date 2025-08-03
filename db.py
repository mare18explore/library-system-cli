import sqlite3

def connect():
    """
    Opens a connection to the local SQLite database file.
    Enables foreign key constraints and returns a cursor/connection.
    """
    # path to db file
    conn = sqlite3.connect("data/library.db") 
    # lets us access rows by column name
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor()
    # ensure FK constraints work
    cur.execute("PRAGMA foreign_keys = ON;")  
    conn.commit()
    return conn, cur
def get_connection():
    """
    Returns a basic DB connection for use cases where a cursor isn't needed immediately.
    """
    conn = sqlite3.connect("data/library.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.commit()
    return conn