# Library System (CLI)

A Python-based command-line library system that allows users to search for books, borrow and return them, pay penalties, and leave reviews. The system also integrates with the [Open Library API](https://openlibrary.org/developers/api) to fetch real book data and populate the catalog.

This is a modular, menu-driven application designed for learning and demo purposes — with support for authentication, penalty tracking, borrowing records, and review features.

## Features

- User login and signup with hashed passwords using bcrypt
- Search books by keyword (title or author)
- Borrow and return books
- Automatic late fee calculation and penalty payment system
- Leave reviews and ratings for books
- Import books from the Open Library API
- Track current borrowings per user
- View global library stats: most borrowed books, top members, highest rated titles, and monthly borrowing activity

## Technologies Used

- Python 3
- SQLite (local file-based DB)
- bcrypt (password hashing)
- Open Library API (book search + metadata)
- colorama for CLI color styling

## How To Run
Clone the repo and install dependencies:

```bash
git clone https://github.com/mare18explore/library-system-cli.git
cd library-system-cli
pip install -r requirements.txt
sqlite3 data/library.db < schema.sql
python3 main.py
```
## Author
Created by Abdi Mare
GitHub: @mare18explore
