
import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sqlite3
from sqlite3 import Error
from db import dbConnection

class tddPython(unittest.TestCase):

    def testStudentTableCreated(self):
        dbConn = dbConnection(":memory:")
        dbConn.createStudentTable()
        try:
            cursor = dbConn.connection.cursor()
            cursor.execute("""SELECT * FROM Students;""")
            tableCreated = True
        except Error:
            tableCreated = False

        dbConn.connection.close()
        self.assertTrue(tableCreated)

    # def testCreateGradeReportTable(self):
    #     self.dbConn = dbConnection(":memory:")
    #     self.dbConn.createTable(self.sqlCreateGradeReportTable)
    #     try:
    #         cursor = self.dbConn.connection.cursor()
    #         cursor.execute("""SELECT * FROM Gradereport;""")
    #         created = True
    #     except Error:
    #         created = False

    #     self.dbConn.connection.close()
    #     self.assertTrue(created)
        
    def testAddStudent(self):
        dbConn = dbConnection(":memory:")
        dbConn.createStudentTable()
        dbConn.addStudent(1,"John", 11)
        cursor = dbConn.connection.cursor()
        cursor.execute("""SELECT * FROM Students;""")
        row = cursor.fetchone()
        dbConn.connection.close()
        self.assertEqual(1,row[0], "IDs did not match")
        self.assertEqual('John',row[1], "Names did not match")

    def testAddStudentGender(self):
        dbConn = dbConnection(":memory:")
        dbConn.createStudentTable()
        dbConn.addStudent(1,"John", 11)
        dbConn.addStudentGender('0001','Male')
        cursor = dbConn.connection.cursor()
        cursor.execute("""SELECT * FROM Students WHERE id = 1;""")
        row = cursor.fetchone()
        dbConn.connection.close()
        self.assertEqual(1,row[0], "IDs did not match")
        self.assertEqual('Male',row[3], "Genders did not match")

    def testGetStudentData(self):
        dbConn = dbConnection(":memory:")
        dbConn.createStudentTable()
        dbConn.addStudent(1,"John",11)
        dbConn.addStudentGender(1,'Male')
        data = dbConn.getStudentData(1)
        firstRow = data[0]
        self.assertEqual(1, firstRow[0], "Student ID did not match")
        self.assertEqual('John', firstRow[1], "Name did not match")
        self.assertEqual(11, firstRow[2], "Gradelevel did not match")
        self.assertEqual('Male', firstRow[3], "Gender did not match")


    # def testAddGradeReport(self):
    #     self.dbConn = dbConnection(":memory:")
    #     self.dbConn.createTable(self.sqlCreateGradeReportTable)
    #     self.dbConn.addGradeReport('0001','1',"01/01/2001","Spring 2022", "3.56", "Classes String", "Honor Roll", "3", "1")
    #     cursor = self.dbConn.connection.cursor()
    #     cursor.execute("""SELECT * FROM Gradereport;""")
    #     row = cursor.fetchone()
    #     self.assertEqual(1, row[0], "ID did not match")
    #     self.assertEqual(1, row[1], "Student ID did not match")
    #     self.assertEqual("01/01/2001",row[2], "Date did not match")
    #     self.assertEqual("Spring 2022",row[3], "Term did not match")
    #     self.assertEqual(3.56,row[4], "GPA did not match")
    #     self.assertEqual("Classes String", row[5], "Classes did not match")
    #     self.assertEqual("Honor Roll", row[6], "Eligibility did not match")
    #     self.assertEqual(3, row[7], "Effort did not match")
    #     self.assertEqual(1, row[8], "Coupons did not match")

if __name__ == '__main__':
    unittest.main()