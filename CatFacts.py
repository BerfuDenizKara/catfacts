import sqlite3
import requests
import json

# Step 1: Set up the SQLite database and table
def setup_database():
    """
    Create an SQLite database and a table to store cat facts if they don't exist.
    """
    try:
        conn = sqlite3.connect('cat_facts.db')  # Connect to SQLite database
        cursor = conn.cursor()
        
        # Create a table with columns id, text, and updatedAt
        cursor.execute('''
                       
            CREATE TABLE IF NOT EXISTS facts2 (
                fact TEXT,
                length INTEGER
            )
        ''')
        
        conn.commit()  # Commit the changes
    except sqlite3.Error as e:
        print(f"An error occurred while setting up the database: {e}")
    finally:
        conn.close()  # Close the connection

setup_database()

# Step 2: Fetch data from the API
def fetch_cat_facts():
    """
    Fetch cat facts from the given API endpoint.
    Returns:
        list: A list of cat facts in JSON format.
    """
    try:
        response = requests.get("https://catfact.ninja/facts")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred while fetching data from the API: {e}")
        return []

cat_facts = fetch_cat_facts()

# Step 3: Store the data in the SQLite database
def store_cat_facts(facts):
    """
    Store the fetched cat facts into the SQLite database.
    
    Args:
        facts (list): List of cat facts in JSON format.
    """
    try:
        conn = sqlite3.connect('cat_facts.db')  # Connect to SQLite database
        cursor = conn.cursor()
        
        # Insert or replace each cat fact in the database
        for fact in facts['data']:
            cursor.execute('''
                INSERT INTO facts2 (fact, length)
                VALUES (?, ?)
            ''', (fact['fact'], fact['length']))
        
        conn.commit()  # Commit the changes
    except sqlite3.Error as e:
        print(f"An error occurred while storing data in the database: {e}")
    finally:
        conn.close()  # Close the connection

store_cat_facts(cat_facts)

# Step 4: Display the data from the database in the console
def display_cat_facts():
    """
    Fetch and display all the cat facts stored in the SQLite database.
    """
    try:
        conn = sqlite3.connect('cat_facts.db')  # Connect to SQLite database
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM facts2')  # Select all rows from the facts table
        rows = cursor.fetchall()  # Fetch all rows
        
        # Display each row in the console
        for row in rows:
            print(f"fact: {row[0]}")
            print(f"length: {row[1]}")
            print("-" * 20)
    except sqlite3.Error as e:
        print(f"An error occurred while fetching data from the database: {e}")
    finally:
        conn.close()  # Close the connection

display_cat_facts()
