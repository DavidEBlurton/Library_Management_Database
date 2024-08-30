# book.py

from database import execute_query

class Book:
    def __init__(self, title, author_id, isbn, publication_date, availability=True):
        self.title = title
        self.author_id = author_id
        self.isbn = isbn
        self.publication_date = publication_date
        self.availability = availability

    def save(self):
        query = """
        INSERT INTO books (title, author_id, isbn, publication_date, availability)
        VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (self.title, self.author_id, self.isbn, self.publication_date, self.availability))
    
    @staticmethod
    def get_by_title(title):
        query = "SELECT * FROM books WHERE title = %s"
        return execute_query(query, (title,), fetchone=True)
    
    @staticmethod
    def get_all():
        query = "SELECT * FROM books"
        return execute_query(query, fetchall=True)

    @staticmethod
    def update_availability(book_id, availability):
        query = "UPDATE books SET availability = %s WHERE id = %s"
        execute_query(query, (availability, book_id))
