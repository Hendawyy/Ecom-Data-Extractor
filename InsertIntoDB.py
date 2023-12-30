import mysql.connector
from mysql.connector import Error

def insert_into_db(title, price, rating, product_link, description, image_sources, category, sold_count, availability):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="AmazonProds"
        )

        cursor = connection.cursor()

        sql_query = """
            INSERT INTO products (
                title, price, rating, product_link, description, image_sources, category, sold_count, availability
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Check if description and image_sources are lists, then join them
        if isinstance(description, list):
            description = ', '.join(description)

        if isinstance(image_sources, list):
            image_sources = ', '.join(image_sources)

        values = (title, price, rating, product_link, description, image_sources, category, sold_count, availability)

        cursor.execute(sql_query, values)

        connection.commit()
        print("Record inserted successfully")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")