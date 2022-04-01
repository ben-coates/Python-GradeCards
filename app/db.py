import sqlite3
from sqlite3 import Error

class dbConnection():
    def __init__(self, connectionPath: str):
        self.connection = sqlite3.connect(connectionPath)

    def createTable(self, sqlcode: str):
        # Create a table form the sql_statement
        try:
            cursor = self.connection.cursor()
            cursor.execute(sqlcode)
        except Error as e:
            print(e)

    def addStudent(self, id, name, gradelevel):
        # Add a student to the table
        try:
            cursor = self.connection.cursor()
            cursor.execute("""INSERT INTO students(id,name,gradelevel) VALUES(?,?,?)""", (id, name, gradelevel))
            self.connection.commit()
        except Error as e:
            print(e)

    def addGradeReport(self, id, studentid, date, term, gpa, classes, eligibility, effort, coupons):
        # Add a student to the table
        try:
            cursor = self.connection.cursor()
            cursor.execute("""INSERT INTO Gradereport(id,studentid,date,term,gpa,classes,eligibility,effort,coupons) VALUES(?,?,?,?,?,?,?,?,?)""", 
                (id, studentid, date, term, gpa, classes, eligibility, effort, coupons))
            self.connection.commit()
        except Error as e:
            print(e)

    def getStudentData(self, studentid):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT * FROM Gradereport WHERE studentid = """ + str(studentid))
            return cursor.fetchall()
        except Error as e:
            print(e)

def main():
    sql_create_student_table = """CREATE TABLE IF NOT EXISTS Students (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        gradelevel integer NOT NULL
                                    );"""

    students = [{'id':'0897','name':'John Doe','gradelevel':'11'}, {'name':'Jane Doe','id':'0896','gradelevel':'12'}, {'name':'Jim Doe','id':'0895','gradelevel':'7'}]

    db = dbConnection(':memory:')
    if db.connection is not None:
        db.createTable(sql_create_student_table)
        for s in students:
            db.addStudent(s.get('id'), s.get('name'), s.get('gradelevel'))

        try:
            cursor = db.connection.cursor()
            cursor.execute("""SELECT id FROM Students""")
            print(cursor.fetchall())
        except Error as e:
            print(e)


if __name__ == "__main__":
    main()