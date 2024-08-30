# database.py

import mysql.connector
from config import DATABASE_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)

def execute_query(query, params=None, fetchone=False, fetchall=False):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    else:
        connection.commit()
        result = None
    cursor.close()
    connection.close()
    return result
