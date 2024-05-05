import os
import csv
import sqlite3
<<<<<<< HEAD
import random 
from dataclasses import dataclass
=======
from dataclasses import dataclass

@dataclass
class Entity:
    name: str
    canonical: bool
>>>>>>> ee945f9275d6b0ae541c51738e04ba5b0b5ae75f

@dataclass
class Message:
    message_content: str
    source_platform: str | None = None
    date_posted: str | None = None
    author_name: str | None = None
    author_id: int | None = None

@dataclass
class Author:
    author_name: str | None = None
    platform_name: str | None = None
    platform_handle: str | None = None 
    age: int | None = None

def setup_database(conn, cursor):
    c = cursor
    c.execute('''CREATE TABLE IF NOT EXISTS Messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_content TEXT NOT NULL, 
                source_platform TINYTEXT DEFAULT NULL,
                date_posted DATETIME, 
                author_name TINYTEXT DEFAULT NULL, 
                author_id INTEGER DEFAULT NULL, 
                FOREIGN KEY (author_id) REFERENCES Authors(author_id)
            )''')
    

    c.execute('''CREATE TABLE IF NOT EXISTS Authors (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_name TINYTEXT DEFAULT NULL,
                platform_name TINYTEXT DEFAULT NULL,
                platform_handle TINYTEXT UNIQUE,
                age INTEGER DEFAULT NULL,
                nationality TINYTEXT DEFAULT NULL,
                province TINYTEXT DEFAULT NULL

            )''')
    #Entities can have different names, like msft, microsot, micsoft. We need to have a canonical name for each entity. Figure out a way to normalize before inserting into db.
    c.execute('''CREATE TABLE IF NOT EXISTS Entities (
                entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                canonical_name TINYTEXT
            )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS EntitySentiments (
              message_id INTEGER NOT NULL,
              entity_id INTEGER NOT NULL,
              sentiment INTEGER NOT NULL,
              date_posted DATETIME,
              foreign key (message_id) references Messages(message_id),
              foreign key (entity_id) references Entities(entity_id)
              PRIMARY KEY (message_id, entity_id)
              )''')
    
    conn.commit()


def get_or_insert_entity(conn, cursor, entity_name): #Check if entity is already in db, if yes, returns entity_id. if not, returns -1. 
    c = cursor
    c.execute('''SELECT entity_id FROM Entities WHERE canonical_name = ?''', (entity_name,)) #Check if entity is already in db
    presence = c.fetchone()
    if presence:
        return presence[0]
    else:
        c.execute('''INSERT INTO Entities (canonical_name) VALUES (?)''', (entity_name,))
        conn.commit()
        return c.lastrowid
        


def insert_message(conn, cursor, message: Message):
    c = cursor
    c.execute('''INSERT INTO Messages (message_content, source_platform, date_posted, author_name, author_id) VALUES (?, ?, ?, ?, ?)''', (message.message_content, message.source_platform, message.date_posted, message.author_name, message.author_id))
    conn.commit()
    return c.lastrowid


def get_or_insert_author_id(conn, cursor, platform_handle):
    c = cursor
    c.execute('''SELECT author_id FROM Authors WHERE platform_handle = ?''', (platform_handle,))
    presence = c.fetchone()
    if presence:
        return presence[0]
    else:
        c.execute('''INSERT INTO Authors (platform_handle) VALUES (?)''', (platform_handle,))
        conn.commit()
        return c.lastrowid
    




def insert_entity_sentiment(conn, cursor, message_id, entity_id, sentiment):
    c = cursor
    c.execute('''INSERT INTO EntitySentiments (message_id, entity_id, sentiment) VALUES (?, ?, ?)''', (message_id, entity_id, sentiment))

def main():
    conn = sqlite3.connect('socialmedia.db')
    c = conn.cursor()
    # Test inserting an author
    platform_handle = 'testuser'
    message = None 

    author_id = get_or_insert_author_id(conn, c, platform_handle)

    message_id = insert_message(conn, c, message) 

    entity_id = get_or_insert_entity(conn, c, entity_name)

    insert_entity_sentiment(conn, c, message_id, entity_id, sentiment)


    conn.close()

if __name__ == "__main__":
    main()
    
