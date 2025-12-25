import mysql.connector
from mysql.connector import Error
def get_db_connection():
    try:
        db_conn = mysql.connector.connect(
        host="localhost",
        user="ecommerce_user",
        password="secure_password",
        database="ecommerce_system" 
        )
        print("Connected to MySQL database")
        return db_conn

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        exit(1)


