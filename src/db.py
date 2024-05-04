import os
import csv
import sqlite3
from dataclasses import dataclass

@dataclass
class Entity:
    name: str
    canonical: bool

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


def check_entity_existence(entity_name: str) -> str | None: #Check if entity is already in db, if yes, returns entity_id. if not, returns None. 
    conn = sqlite3.connect('socialmedia.db')
    c = conn.cursor()
    c.execute('''SELECT entity_id FROM entities WHERE name = ?''', (entity_name,)) #Check if entity is already in db
    presence = c.fetchone()
    if presence:
        return presence[0]
    else:
        return None
    
def get_example_of_entity(entity_name: str): #Get an example of a snippet where the entity is mentioned
    conn = sqlite3.connect('socialmedia.db')
    c = conn.cursor()
    c.execute('''SELECT snippet FROM snippets WHERE entity = ?''', (entity_name,))
    example = c.fetchone()
    return example[0]

        

if __name__ == "__main__":
   # setup_database()
   # print("Database setup complete.")