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
        5. Exit/Quit
        """)
        ans=input("Please enter your selection: ") 
        if ans=="1": 
            search()
        elif ans=="2":
     #       insert()
            print("insert")
        elif ans=="3":
     #       modify()
            print("modify")
        elif ans=="4":
       #     delete()
            print("delete")
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
    db.autocommit = True
    return
def search():
    ans=True
    print ("""
    1. Artists
    2. Genre
    3. Keyword
    """)
    ans=input("Please enter your selection: ") 
    if ans=="1": 
        fin = input("Please enter the artist name: ")
        query = """SELECT album.id as alID, name, title, year FROM (SELECT * FROM artist where name = %s) as subquery JOIN album ON album.artist_id=subquery.id"""
    elif ans=="2":
        fin = input("Please enter the genre: ")
        query = """SELECT album_id, name, title, year FROM ((SELECT * FROM album_genre where genre = %s) as subquery JOIN album ON album.id=subquery.album_id) as subquery2 JOIN artist on artist.id=subquery2.artist_id"""
    elif ans=="3":
        fin = input("Please enter the keyword: ")
#         query = """SELECT name, title, year FROM (SELECT * FROM artist where name = %s) as subquery JOIN album ON album.id=subquery.id"""
    elif ans !="":
        print("Invalid selection. Try again.")
        search()

    cursor.execute(query, (fin,));

    results = cursor.fetchall()

    print("\n ID \t Artist \t \t Album \t \t \t Year")
    for row in results:
        alID, name, title, year = row
        print(alID, "\t", name, "\t", title, "\t", year)

#def insert():

#def modify():

#def delete():

if __name__ == '__main__':                          # run main on start
    main()
