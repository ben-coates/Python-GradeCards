import sqlite3
from sqlite3 import Error
from progressReport import ProgressReport

class dbConnection():
    def __init__(self, connectionPath: str):
        self.connection = sqlite3.connect(connectionPath)

    def createStudentTable(self):
        sql_create_student_table = """CREATE TABLE IF NOT EXISTS Students (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        gradelevel integer NOT NULL,
                                        gender text,
                                        CHECK (gender = 'Female' OR 'Male')
                                    );"""
        
        # Create the student table fromm the sql_statement
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_create_student_table)
        except Error as e:
            print(e)

    def addStudent(self, id, name, gradelevel):
        # Add a student to the table
        try:
            cursor = self.connection.cursor()
            cursor.execute("""INSERT OR REPLACE INTO Students(id,name,gradelevel) VALUES(?,?,?)""", (id, name, gradelevel))
            self.connection.commit()
        except Error as e:
            print(e)

    def addStudentGender(self, id, gender):
        # Add a student to the table
        try:
            cursor = self.connection.cursor()
            cursor.execute("""UPDATE Students SET gender = ? WHERE id = ?""", (gender, id))
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
            cursor.execute("""SELECT * FROM Students WHERE id = ?""", str(studentid))
            return cursor.fetchall()
        except Error as e:
            print(e)

def main():
    sql_create_student_table = """CREATE TABLE IF NOT EXISTS Students (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        gradelevel integer NOT NULL,
                                        gender text,
                                        CHECK (gender = 'Male' OR 'Female')
                                    );"""

    rawText = open('report.txt').read()
    pReport = ProgressReport(rawText)
    print("students list")
    print(pReport.data)


    db = dbConnection(':memory:')
    if db.connection is not None:
        db.createStudentTable()
        for s in pReport.data:
            db.addStudent(s.id, s.name, s.gradelevel)

        try:
            cursor = db.connection.cursor()
            cursor.execute("""SELECT * FROM Students""")
            for i in cursor.fetchall():
                print(i)
        except Error as e:
            print(e)
    else: 
        print("No database")


if __name__ == "__main__":
    main()