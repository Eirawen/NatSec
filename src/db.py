import os
import csv
import sqlite3

def setup_database():
    conn = sqlite3.connect('socialmedia.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entities
                 (entiy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, 
                  canonical TINYTEXT,
                  positive_count INTEGER, 
                  negative_count INTEGER, 
                  neutral_count INTEGER, 
                  sentiment TINYTEXT, 
                  last_updated TEXT)''')
    conn.commit()
    conn.close()


def check_entity_existence(entity_name): #Check if entity is already in db, if yes, returns entity_id. if not, returns -1. 
    conn = sqlite3.connect('socialmedia.db')
    c = conn.cursor()
    c.execute('''SELECT entity_id FROM entities WHERE name = ?''', (entity_name,)) #Check if entity is already in db
    presence = c.fetchone()
    if presence:
        return presence[0]
    else:
        return -1
        

if __name__ == "__main__":
   # setup_database()
   # print("Database setup complete.")