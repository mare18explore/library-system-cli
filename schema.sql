DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS borrowings;
DROP TABLE IF EXISTS penalties;
DROP TABLE IF EXISTS reviews;

CREATE TABLE members (
  email TEXT PRIMARY KEY,
  passwd TEXT NOT NULL,
  name TEXT NOT NULL,
  byear INTEGER,
  faculty TEXT
);

CREATE TABLE books (
  book_id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT,
  pyear INTEGER
);

CREATE TABLE borrowings (
  bid INTEGER PRIMARY KEY,
  member TEXT,
  book_id INTEGER,
  start_date DATE,
  end_date DATE,
  FOREIGN KEY(member) REFERENCES members(email),
  FOREIGN KEY(book_id) REFERENCES books(book_id)
);

CREATE TABLE penalties (
  pid INTEGER PRIMARY KEY,
  bid INTEGER,
  amount INTEGER NOT NULL,
  paid_amount INTEGER,
  FOREIGN KEY(bid) REFERENCES borrowings(bid)
);

CREATE TABLE reviews (
  rid INTEGER PRIMARY KEY,
  book_id INTEGER,
  member TEXT,
  rating INTEGER,
  rtext TEXT,
  rdate DATE,
  FOREIGN KEY(book_id) REFERENCES books(book_id),
  FOREIGN KEY(member) REFERENCES members(email)
);