import os
import csv
import sqlite3

def setup_database():
    conn = sqlite3.connect('socialmedia.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entities
                 (name TEXT, canonical TINYTEXT, positive_count INTEGER, negative_count INTEGER, neutral_count INTEGER, sentiment TINYTEXT, last_updated TEXT)''')
    conn.commit()
    conn.close()




if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")