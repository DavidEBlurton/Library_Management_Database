# author.py

from database import execute_query

class Author:
    def __init__(self, name, biography):
        self.name = name
        self.biography = biography

    def save(self):
        query = """
        INSERT INTO authors (name, biography)
        VALUES (%s, %s)
        """
        execute_query(query, (self.name, self.biography))

    @staticmethod
    def get_by_name(name):
        query = "SELECT * FROM authors WHERE name = %s"
        return execute_query(query, (name,), fetchone=True)

    @staticmethod
    def get_all():
        query = "SELECT * FROM authors"
        return execute_query(query, fetchall=True)
