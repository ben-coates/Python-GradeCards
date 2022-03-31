import sqlite3
from sqlite3 import Error

sql_create_student_table = """CREATE TABLE IF NOT EXISTS students (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                gradelevel integer NOT NULL
                            );"""

sql_add_student = """INSERT INTO students(id,name,gradelevel) VALUES(?,?,?)"""

def createTable(connection: sqlite3.Connection, sqlcode: str):
    # Create a table form the sql_statement
    try:
        cursor = connection.cursor()
        cursor.execute(sqlcode)
    except Error as e:
        print(e)

def addStudent(connection: sqlite3.Connection, sqlcode: str, studentInfo):
    # Add a student to the table
    try:
        cursor = connection.cursor()
        cursor.execute(sqlcode, studentInfo)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)

def exportData(students):
    connection = sqlite3.connect("data.db")

    if connection is not None:
        createTable(connection, sql_create_student_table)
        for s in students:
            addStudent(connection, sql_add_student, (s.id, s.name, s.gradelevel))

    try:
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM students;""")
    except Error as e:
        print(e)
    
