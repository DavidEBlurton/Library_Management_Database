# main.py

from book import Book
from user import User
from author import Author
from database import execute_query

def display_menu():
    print('''\nWelcome to the Library Management System!
    Main Menu:
    1. Book Operations
    2. User Operations
    3. Author Operations
    4. Quit''')

def book_operations():
    print('''\nBook Operations:
    1. Add a new book
    2. Borrow a book
    3. Return a book
    4. Search for a book
    5. Display all books''')

def user_operations():
    print('''\nUser Operations:
    1. Add a new user
    2. View user details
    3. Display all users''')

def author_operations():
    print('''\nAuthor Operations:
    1. Add a new author
    2. View author details
    3. Display all authors''')

def add_book():
    title = input("Enter the book title: ")
    author_name = input("Enter the author name: ")
    isbn = input("Enter the ISBN: ")
    publication_date = input("Enter the publication date (YYYY-MM-DD): ")
    
    author = Author.get_by_name(author_name)
    if not author:
        print("Author not found. Please add the author first.")
        return

    author_id = author['id']
    book = Book(title, author_id, isbn, publication_date)
    book.save()
    print("Book added successfully.")

def borrow_book():
    title = input("Enter the title of the book to borrow: ")
    book = Book.get_by_title(title)
    if not book or not book['availability']:
        print("Book not available or not found.")
        return

    library_id = input("Enter your library ID: ")
    user = User.get_by_library_id(library_id)
    if not user:
        print("User ID not found.")
        return

    book_id = book['id']
    user_id = user['id']
    borrow_date = '2024-08-30'  # This should ideally be the current date
    
    query = """
    INSERT INTO borrowed_books (user_id, book_id, borrow_date)
    VALUES (%s, %s, %s)
    """
    execute_query(query, (user_id, book_id, borrow_date))
    Book.update_availability(book_id, False)
    print("Book borrowed successfully.")

def return_book():
    title = input("Enter the title of the book to return: ")
    book = Book.get_by_title(title)
    if not book or book['availability']:
        print("Book not found or already available.")
        return

    library_id = input("Enter your library ID: ")
    user = User.get_by_library_id(library_id)
    if not user:
        print("User ID not found.")
        return

    book_id = book['id']
    user_id = user['id']
    
    query = """
    UPDATE borrowed_books
    SET return_date = %s
    WHERE book_id = %s AND user_id = %s AND return_date IS NULL
    """
    execute_query(query, ('2024-08-30', book_id, user_id))
    Book.update_availability(book_id, True)
    print("Book returned successfully.")

def search_book():
    title = input("Enter the title of the book to search: ")
    book = Book.get_by_title(title)
    if book:
        print(book)
    else:
        print("Book not found.")

def display_all_books():
    books = Book.get_all()
    if not books:
        print("No books in the library.")
    for book in books:
        print(book)

def add_user():
    name = input("Enter the user's name: ")
    library_id = input("Enter the library ID: ")
    user = User(name, library_id)
    user.save()
    print("User added successfully.")

def view_user():
    library_id = input("Enter the library ID to view details: ")
    user = User.get_by_library_id(library_id)
    if user:
        print(f"Name: {user['name']}, Library ID: {user['library_id']}")
        # Retrieve and display borrowed books
        query = """
        SELECT books.title
        FROM borrowed_books
        JOIN books ON borrowed_books.book_id = books.id
        WHERE borrowed_books.user_id = %s AND borrowed_books.return_date IS NULL
        """
        borrowed_books = execute_query(query, (user['id'],), fetchall=True)
        if borrowed_books:
            print("Borrowed Books:")
            for book in borrowed_books:
                print(f" - {book['title']}")
        else:
            print("No borrowed books.")
    else:
        print("User not found.")

def display_all_users():
    users = User.get_all()
    if not users:
        print("No users in the system.")
    for user in users:
        print(f"Name: {user['name']}, Library ID: {user['library_id']}")

def add_author():
    name = input("Enter the author's name: ")
    biography = input("Enter the author's biography: ")
    author = Author(name, biography)
    author.save()
    print("Author added successfully.")

def view_author():
    name = input("Enter the author's name to view details: ")
    author = Author.get_by_name(name)
    if author:
        print(f"Name: {author['name']}, Biography: {author['biography']}")
    else:
        print("Author not found.")

def display_all_authors():
    authors = Author.get_all()
    if not authors:
        print("No authors in the system.")
    for author in authors:
        print(f"Name: {author['name']}, Biography: {author['biography']}")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            book_operations()
            book_choice = input("Enter your choice: ")
            if book_choice == '1':
                add_book()
            elif book_choice == '2':
                borrow_book()
            elif book_choice == '3':
                return_book()
            elif book_choice == '4':
                search_book()
            elif book_choice == '5':
                display_all_books()
            else:
                print("Invalid choice.")

        elif choice == '2':
            user_operations()
            user_choice = input("Enter your choice: ")
            if user_choice == '1':
                add_user()
            elif user_choice == '2':
                view_user()
            elif user_choice == '3':
                display_all_users()
            else:
                print("Invalid choice.")

        elif choice == '3':
            author_operations()
            author_choice = input("Enter your choice: ")
            if author_choice == '1':
                add_author()
            elif author_choice == '2':
                view_author()
            elif author_choice == '3':
                display_all_authors()
            else:
                print("Invalid choice.")

        elif choice == '4':
            print("Quitting the application.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

