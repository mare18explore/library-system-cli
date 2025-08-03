from modules.auth import login_user, signup_user, is_valid_email, is_valid_name, is_valid_faculty, account_exists
from modules.books import search_books, borrow_book, return_book
from modules.penalties import get_unpaid_penalties, pay_penalty, create_penalty
from modules.reviews import leave_review
from modules.import_books import fetch_books_from_api, insert_books_into_db
from modules.dashboard import get_active_borrowings
from colorama import init, Fore
import getpass
from modules.dashboard import show_library_stats

# Enable auto color reset after each print
init(autoreset=True)

def login_or_signup():
  """
  Let user login or sign up.
  Return user email if successful, else None.
  """
  while True:
    print(Fore.CYAN + "\n1. Login\n2. Sign Up\n3. Quit")
    choice = input("Choose an option: ").strip()

    if choice == '1':
      email = input("Email: ").strip()
      password = getpass.getpass("Password: ").strip()
      if not password:
        print("Password cannot be empty.")
        continue

      if login_user(email, password):
        print(Fore.GREEN + f"\nWelcome back, {email}!")
        return email
      else:
        print(Fore.RED + "Login failed. Please try again.")

    elif choice == '2':
      email = input("Email: ").strip()
      if not is_valid_email(email):
        print("Invalid email format.")
        continue
      if account_exists(email):
        print("An account with that email already exists.")
        continue

      password = getpass.getpass("Password: ").strip()
      name = input("Name (no spaces): ").strip()
      if not is_valid_name(name):
        print("Invalid name.")
        continue

      try:
        byear = int(input("Birth year: "))
        if byear < 1900 or byear > 2025:
          raise ValueError
      except ValueError:
        print("Birth year must be a number between 1900 and 2025.")
        continue

      faculty = input("Faculty: ").strip()
      if not is_valid_faculty(faculty):
        print("Invalid faculty name.")
        continue

      if signup_user(email, password, name, byear, faculty):
        print(f"Account created! Welcome, {email}")
        return email
      else:
        print("Signup failed. Please try again.")

    elif choice == '3':
      print(Fore.CYAN + "See you next time! Thanks for using the Library System.")
      return None

    else:
      print(Fore.RED + "Invalid option. Try again.")


def user_dashboard(email):
  """
  Dashboard after login. Let user search, borrow, return, view penalties, etc.
  """
  while True:
    print(Fore.YELLOW + f"\n== Welcome, {email} ==")
    print(Fore.BLUE + "1. Search Books")
    print(Fore.BLUE + "2. Return Book")
    print(Fore.BLUE + "3. View & Pay Penalties")
    print(Fore.BLUE + "4. Logout")
    print(Fore.BLUE + "5. Import Books from API")
    print(Fore.BLUE + "6. View Current Borrowings")
    print(Fore.GREEN + "7. View Library Stats")

    choice = input("Choose an option: ").strip()

    if choice == '1':
      keyword = input("Enter keyword (title or author): ")
      results = search_books(keyword)

      if not results:
        print("No matches found.")
        continue

      print("\nSearch Results:")
      for book in results:
        status_color = Fore.GREEN if book['availability'] == 'Available' else Fore.RED
        print(f"{Fore.YELLOW}[{book['book_id']}] {book['title']} by {book['author']} ({book['pyear']}) | Rating: {book['avg_rating']} | {status_color}{book['availability']}")

      book_id = input("\nEnter Book ID to borrow or press Enter to cancel: ").strip()
      if book_id.isdigit():
        result = borrow_book(int(book_id), email)
        if result is True:
          print(Fore.GREEN + "Book borrowed successfully!")
        else:
          print(Fore.RED + result)  # Error message from books.py
      else:
        print("Cancelled.")

    elif choice == '2':
      bid = input("Enter your borrowing ID to return: ").strip()
      if not bid.isdigit():
        print("Invalid borrowing ID.")
        continue

      late_days = return_book(int(bid), email)
      if late_days is None:
        print("You have no active borrowing with that ID.")
      elif late_days == 0:
        print(Fore.GREEN + "Book returned on time. Thanks!")
      else:
        print(f"Returned {late_days} days late. Penalty of ${late_days} applied.")
        pid = create_penalty(int(bid), late_days)
        print(f"Penalty ID: {pid}")

      review_choice = input("Would you like to leave a review? (y/n): ").strip().lower()
      if review_choice == 'y':
        try:
          rating = int(input("Rating (1–5): "))
          review_text = input("Review: ").strip()
          leave_review(email, int(bid), rating, review_text)
          print("Thanks for reviewing!")
        except ValueError:
          print("Invalid rating or review skipped.")

    elif choice == '3':
      penalties = get_unpaid_penalties(email)
      if not penalties:
        print(Fore.GREEN + "No unpaid penalties.")
        continue

      print("\nYour Penalties:")
      for p in penalties:
        due = p["amount"]
        paid = p["paid"]
        print(f"ID: {p['pid']} | Amount: ${due} | Paid: ${paid} | Owing: ${due - paid}")

      pid = input("Enter penalty ID to pay or press Enter to cancel: ").strip()
      if pid.isdigit():
        amount = input("Amount to pay: ").strip()
        if amount.isdigit():
          pay_penalty(int(pid), int(amount))
          print(Fore.GREEN + "Payment recorded.")
        else:
          print("Invalid amount.")
      else:
        print("Cancelled.")

    elif choice == '4':
      print("Logged out.\n")
      break

    elif choice == '5':
      print("\n=== Import Books from Open Library API ===")
      keyword = input("Enter a keyword (e.g. 'fantasy', 'history', 'python'): ").strip()
      if not keyword:
        print("No keyword entered. Returning to menu.")
        continue

      books = fetch_books_from_api(keyword)
      books = books[:20]  # Limit to first 20 results

      if not books:
        print("No books found or API failed.")
      else:
        insert_books_into_db(books)
        print(Fore.GREEN + f"Imported {len(books)} books from Open Library.")
        print("Sample:")
        for b in books[:3]:  # Preview first 3 entries
          print(f"- {b['title']} by {b['author']}")

    elif choice == '6':
      records = get_active_borrowings(email)
      if not records:
        print("You have no active borrowings.")
      else:
        print("\nYour Current Borrowings:")
        for r in records:
          print(f"Borrow ID: {r['bid']} | Title: {r['title']} | Borrowed On: {r['start_date']}")
    
    elif choice == '7':
      show_library_stats()

    else:
      print(Fore.RED + "Invalid option. Please choose between 1–6.")


def main():
  print(Fore.MAGENTA + "=== Library Management System ===")
  while True:
    user = login_or_signup()
    if not user:
      break
    user_dashboard(user)


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(Fore.RED + f"\nUnexpected error: {e}")