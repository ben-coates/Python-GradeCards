
import unittest
import sqlite3
from sqlite3 import Error
from db import dbConnection

class tddPython(unittest.TestCase):
    sqlCreateStudentTable = """CREATE TABLE IF NOT EXISTS Students (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        gradelevel integer NOT NULL
                                    );"""
    
    sqlCreateGradeReportTable = """CREATE TABLE IF NOT EXISTS Gradereport (
                                        id integer PRIMARY KEY,
                                        studentid integer SECONDARY KEY,
                                        date text NOT NULL,
                                        term text NOT NULL,
                                        gpa float NOT NULL,
                                        classes text NOT NULL,
                                        eligibility text NOT NULL,
                                        effort integer NOT NULL,
                                        coupons integer NOT NULL
                                    );"""

    def testCreateStudentTable(self):
        self.dbConn = dbConnection(":memory:")
        self.dbConn.createTable(self.sqlCreateStudentTable)
        try:
            cursor = self.dbConn.connection.cursor()
            cursor.execute("""SELECT * FROM Students;""")
            created = True
        except Error:
            created = False

        self.dbConn.connection.close()
        self.assertTrue(created)

    def testCreateGradeReportTable(self):
        self.dbConn = dbConnection(":memory:")
        self.dbConn.createTable(self.sqlCreateGradeReportTable)
        try:
            cursor = self.dbConn.connection.cursor()
            cursor.execute("""SELECT * FROM Gradereport;""")
            created = True
        except Error:
            created = False

        self.dbConn.connection.close()
        self.assertTrue(created)
        
    def testAddStudent(self):
        self.dbConn = dbConnection(":memory:")
        self.dbConn.createTable(self.sqlCreateStudentTable)
        self.dbConn.addStudent('0001',"John","11")
        cursor = self.dbConn.connection.cursor()
        cursor.execute("""SELECT * FROM Students;""")
        row = cursor.fetchone()
        self.assertEqual(1,row[0], "IDs did not match")
        self.assertEqual('John',row[1], "Names did not match")
        self.assertEqual(11,row[2], "Gradelevels did not match")

    def testGetStudentData(self):
        self.dbConn = dbConnection(":memory:")
        self.dbConn.createTable(self.sqlCreateStudentTable)
        self.dbConn.addStudent('0001',"John","11")
        self.dbConn.createTable(self.sqlCreateGradeReportTable)
        self.dbConn.addGradeReport('0001','0001',"01/01/2001","Spring 2022", "3.56", "Classes String", "Honor Roll", "3", "1")
        data = self.dbConn.getStudentData(1)
        firstRow = data[0]
        self.assertEqual(1, firstRow[0], "ID did not match")
        self.assertEqual(1, firstRow[1], "Student ID did not match")
        self.assertEqual("01/01/2001", firstRow[2], "Date did not match")
        self.assertEqual("Spring 2022", firstRow[3], "Term did not match")
        self.assertEqual(3.56, firstRow[4], "GPA did not match")
        self.assertEqual("Classes String", firstRow[5], "Classes did not match")
        self.assertEqual("Honor Roll", firstRow[6], "Eligibility did not match")
        self.assertEqual(3, firstRow[7], "Effort did not match")
        self.assertEqual(1, firstRow[8], "Coupons did not match")

    def testAddGradeReport(self):
        self.dbConn = dbConnection(":memory:")
        self.dbConn.createTable(self.sqlCreateGradeReportTable)
        self.dbConn.addGradeReport('0001','1',"01/01/2001","Spring 2022", "3.56", "Classes String", "Honor Roll", "3", "1")
        cursor = self.dbConn.connection.cursor()
        cursor.execute("""SELECT * FROM Gradereport;""")
        row = cursor.fetchone()
        self.assertEqual(1, row[0], "ID did not match")
        self.assertEqual(1, row[1], "Student ID did not match")
        self.assertEqual("01/01/2001",row[2], "Date did not match")
        self.assertEqual("Spring 2022",row[3], "Term did not match")
        self.assertEqual(3.56,row[4], "GPA did not match")
        self.assertEqual("Classes String", row[5], "Classes did not match")
        self.assertEqual("Honor Roll", row[6], "Eligibility did not match")
        self.assertEqual(3, row[7], "Effort did not match")
        self.assertEqual(1, row[8], "Coupons did not match")

if __name__ == '__main__':
    unittest.main()