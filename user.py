# user.py

from database import execute_query

class User:
    def __init__(self, name, library_id):
        self.name = name
        self.library_id = library_id

    def save(self):
        query = """
        INSERT INTO users (name, library_id)
        VALUES (%s, %s)
        """
        execute_query(query, (self.name, self.library_id))

    @staticmethod
    def get_by_library_id(library_id):
        query = "SELECT * FROM users WHERE library_id = %s"
        return execute_query(query, (library_id,), fetchone=True)

    @staticmethod
    def get_all():
        query = "SELECT * FROM users"
        return execute_query(query, fetchall=True)
