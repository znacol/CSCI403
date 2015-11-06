#!/usr/bin/python3

# Zoe Nacol
# Colorado School of Mines
# CSCI 403 Fall 2015
# Project 05
#
# Some code taken from C. Painter-Wakefield's provided example.py file

import getpass
import pg8000

def main():
    connect() 
    
    ans=True
    while ans:
        print ("""
        1. Search
        2. Insert
        3. Modify
        4. Delete
        5. Exit
        """)
        ans=input("Please enter your selection: ") 
        if ans=="1": 
            search()
        elif ans=="2":
            insert()
        elif ans=="3":
            modify()
        elif ans=="4":
            delete()
        elif ans=="5":
            ans=None
        elif ans !="":
            print("Invalid selection. Try again.")
    cursor.close()
    db.close()

# Connects to database
def connect():
    login = input('login: ')
    secret = getpass.getpass('password: ')

    credentials = {'user'    : login, 
                   'password': secret, 
                   'database': 'csci403',
                   'host'    : 'flowers.mines.edu'}

    try:
        global db
        db = pg8000.connect(**credentials)
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        exit()
    global cursor
    cursor = db.cursor()
    return

def search():
    ans=True
    print ("""
    1. Artists
    2. Genre
    3. Keyword
    """)
    ans=input("Please select a method to search for albums: ") 
    if ans=="1": 
        fin = input("Please enter the artist name: ")
        query = """SELECT album.id as alID, name, title, year FROM
        (SELECT * FROM artist where name = %s) as subquery
        JOIN album ON album.artist_id=subquery.id"""
    elif ans=="2":
        fin = input("Please enter the genre: ")
        query = """SELECT album_id, name, title, year
        FROM ((SELECT * FROM album_genre where genre = %s) as subquery
        JOIN album ON album.id=subquery.album_id) as subquery2
        JOIN artist on artist.id=subquery2.artist_id"""
    elif ans=="3":
        fin = input("Please enter the keyword (case insensitive): ")
        fin = '%' + fin + '%'
        query = """SELECT subquery.id, name, title, year FROM
                (SELECT * FROM album WHERE UPPER(title) LIKE UPPER(%s)) as subquery
                JOIN artist ON artist.id=subquery.artist_id"""
    elif ans !="":
        print("Invalid selection. Try again.")
        search()
        return

    try:
       cursor.execute(query, (fin,));
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])
    
    results = cursor.fetchall()

    print("\n ID \t Artist \t \t Album \t \t \t Year")
    i = 0
    for row in results:
        alID, name, title, year = row
        print(alID, "\t", name, "\t \t", title, "\t", year)
        i=i+1
    print("\n", i, " results found!")


def insert():
    searchArtist()
    artist = input("Please enter an artist ID: ")
    title = input("Please enter an album title: ")
    year = input("Please enter the album's year: ")
    genres = input("Please enter the album's genres: ")
    query = """INSERT INTO album (artist_id, title, year)
            VALUES (%s, %s, %s) """                                     # insert values into album
    try:
       cursor.execute(query, (artist, title, year));
       db.commit()
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])
        db.rollback()

    query = """SELECT id FROM album WHERE artist_id = %s AND title = %s AND year = %s"""        # get album id
    try:
       cursor.execute(query, (artist, title, year));
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])

    album_id, = cursor.fetchone()
    genre_list = genres.split(',')
    for g in genre_list:
        insertAlbumGenre(album_id, g.strip())

def searchArtist():                                                     # displays artists and their IDs
    query = """SELECT id, name FROM artist"""

    try:
       cursor.execute(query);
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])
    
    results = cursor.fetchall()
    i = 0
    print("\n ID \t Artist")
    for row in results:
        id, name = row
        i = i + 1
        print(id, "\t", name)

    print("\n",  i, " results found!")
def insertAlbumGenre(album_id, genre):                                  # inserts genre(s) into album_genre
    query = """INSERT INTO album_genre (album_id, genre)
            VALUES (%s, %s)"""
    try:
        cursor.execute(query, (album_id, genre));
        db.commit()
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])
        db.rollback()

def modify():
    search()
    alId = input("Please enter an album ID to modify: ")

    # print genres
    query = """SELECT genre FROM album_genre WHERE album_id = %s"""

    try:
        cursor.execute(query, (alId, ));
        db.commit()
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])
        db.rollback()
    ans=True
    while ans:                                                              # modify menu loops until user says to exit
        print("""
            1. Title
            2. Year
            3. Genre List
            4. Go back to main menu
            """)
        ans=input("Please enter what value you would like to modify: ")
        if ans=="1":
            fin=input("Please enter title: ")
            query = """UPDATE album SET title = %s WHERE id = %s"""
        elif ans=="2":
            fin=input("Please enter year: ")
            query = """UPDATE album SET year = %s WHERE id = %s"""
        elif ans==3:
            fin=input("Please enter genre(s) separated by commas: ")
            query = """UPDATE album SET title = %s WHERE id = %s"""
        elif ans=="4":
            return
        elif ans!="":
            print("Invalid Selection. Please try again.")
            return

        try:
            cursor.execute(query, (fin, alId));
            db.commit()
        except pg8000.Error as e:
            print('Databse Error: ', e.args[2])
            db.rollback()
def delete():
    search()
    alId = input("Please enter an album ID to delete: ")
    
    query = """DELETE FROM album_genre WHERE album_id=%s"""
    try:
        cursor.execute(query, (alId,));
        db.commit()
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])
        db.rollback()

    query = """DELETE FROM album WHERE id=%s"""
    try:
        cursor.execute(query, (alId,));
        db.commit()
    except pg8000.Error as e:
        print('Databse Error: ', e.args[2])
        db.rollback()
if __name__ == '__main__':                          # run main on start
    main()
