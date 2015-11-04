#!/usr/bin/python3
# Zoe Nacol
# CSCI 403 Fall 2015
# Project 05
#
# Some code taken from C. Painter-Wakefield's provided example file
# Modified: 10/31/2015

import getpass
import pg8000

def main():
    cursor = db.cursor()
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
        ans=raw_input("Please enter your selection") 
        if ans=="1": 
            search()
            print("\n Search") 
        elif ans=="2":
            insert()
            print("\n Insert") 
        elif ans=="3":
            modify()
            print("\n Modify") 
        elif ans=="4":
            delete()
            print("\n Delete") 
        elif ans=="5":
            print("\n Exiting!")
            ans=None
        elif ans !="":
            print("\n Not Valid Choice Try again")
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
        db = pg8000.connect(**credentials)
    except pg8000.Error as e:
        print('Database error: ', e.args[2])
        exit()

    # uncomment next line if you want every insert/update/delete to immediately
    # be applied; you can remove all db.commit() and db.rollback() statements
    db.autocommit = True
    return
def search();
        ans=True
        print ("""
        1. Artists
        2. Genre
        3. Keyword
        """)
        ans=raw_input("Please enter your selection: ") 
        if ans=="1": 
            print("\n Please enter the artist name: ")
            print("\n Search by artist") 
        elif ans=="2":
            print("\n Please enter the genre: ")
            print("\n Search by genre") 
        elif ans=="3":
            print("\n Please enter the keyword: ")
            print("\n Search by keyword") 
        elif ans !="":
            print("\n Not Valid Choice Try again")
def insert():

def modify():

def delete():



########################################## CPW CODE ################################################
# prepared SELECT
faculty = input('Enter faculty as lastname, firstname: ')
query = """SELECT course_id, section, title 
           FROM mines_courses 
           WHERE instructor = %s"""  

cursor.execute(query, (faculty,));

results = cursor.fetchall()
for row in results:
    course_id, section, title = row
    print(course_id, section, title)

# modification queries with exception handling
query = "INSERT INTO genre VALUES (%s)"
try:
    cursor.execute(query, ('celtic',))
    db.commit()
except pg8000.Error as e:
    print('Database error: ', e.args[2])

# second time should cause an integrity constraint violation
try:
    cursor.execute(query, ('celtic',))
    db.commit()
except pg8000.Error as e:
    print('Database error: ', e.args[2])

# bad SELECT query with exception handling
query = "SELECT FROM foo WHERE blah = arg"
try:
    cursor.execute(query)
except pg8000.Error as e:
    print('Database error: ', e.args[2])
