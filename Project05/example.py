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
