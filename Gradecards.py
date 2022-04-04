# Python Library file imports
import os
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QTextEdit, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QIcon
from openpyxl import Workbook

# Program file imports
from deansreport import runDeansReport
from formatGradecards import runGradeCards
from progressReport import ProgressReport
from db import dbConnection

# Get File and add text to the text box
def getFile(textbox: QTextEdit):

    # Request the location of the file to load
    filename = QFileDialog.getOpenFileName(caption = "Open Report", filter = "Text files (*.txt)")

    # As long as the file name is not blank
    if (filename[0] != ''):
        try:
            file = open(filename[0])
            for line in file:
                textbox.insertPlainText(str(line))
        except:
            exeptionMessage = QMessageBox()
            exeptionMessage.setWindowTitle("Error")
            exeptionMessage.setText("File was unable to be opened. Try again. \n If the issue persists contact the program administrator.")
            exeptionMessage.exec()

def saveReport(textbox: QTextEdit):
    # Grab the text from the report excluding the first line until the end
    textProgressReport = textbox.toPlainText()

    # Create a new report from the report class, set students equal to the report data.
    newProgessReport = ProgressReport(textProgressReport)
    addStudentsToDatabase(newProgessReport.data)
    printStudentsFromDatabase(newProgessReport.data)

    # Prompt user to save file and request a save destination
    excelFile = QFileDialog.getSaveFileName(caption = "Save Report", filter = "Excel files (*.xlsx)")
    
    # Create a workbook, run the deans report, run the gradecards, save the file
    workbook = Workbook()
    runDeansReport(newProgessReport.data, workbook)
    runGradeCards(newProgessReport.data, workbook)
    workbook.save(filename=excelFile[0])

    # Report to user that the report has been saved
    savedMessage = QMessageBox()
    savedMessage.setWindowTitle("Report Saved")
    savedMessage.setText("Report has been saved to " + excelFile[0])
    savedMessage.exec()

def addStudentsToDatabase(studentList):
    db = dbConnection('test.db')
    db.createStudentTable()

    for i in studentList:
        db.addStudent(i.id, i.name, i.gradelevel)

def printStudentsFromDatabase(studentList):
    db = dbConnection('test.db')

    for i in studentList:
        gender = str(input("What is the gender of " + i.name + ": "))
        db.addStudentGender(i.id, gender)

    cursor = db.connection.cursor()
    cursor.execute("""SELECT id, name, gender FROM Students'""")
    for i in cursor.fetchall():
        print(i)
    print()

def main():
    # Create the application
    app = QApplication([], )

    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)

    icon = QIcon(os.path.join(application_path, "gradecards.ico"))

    # Create the window GroupBox for the application components, Set the title of the groupbox Widget, Set the title of the overall window
    window = QGroupBox()
    window.setTitle("Progress Report")
    window.setWindowTitle("Gradecards")
    window.setWindowIcon(icon)
    window.resize(500, 500)
    
    # Create a text box and set the default text value
    textbox = QTextEdit()
    textbox.setPlaceholderText("Please load the progress report from a file or copy and paste it here.")
    
    # Create a button for triggering the file load
    fromFileButton = QPushButton("Load from File")
    fromFileButton.clicked.connect(lambda: getFile(textbox))

    # Create a button for triggering the save report
    runReportButton = QPushButton("Run Report")
    runReportButton.clicked.connect(lambda: saveReport(textbox))

    # # Create a button for triggering the save report
    # editStudents = QPushButton("Edit Student List")
    # editStudents.clicked.connect(lambda: printStudentsFromDatabase())

    hbox = QHBoxLayout()
    hbox.addWidget(fromFileButton)
    hbox.addWidget(runReportButton)
    # hbox.addWidget(editStudents)

    # Create the box layout and add the widgets to the layout
    vbox = QVBoxLayout()
    vbox.addWidget(textbox)
    vbox.addLayout(hbox)
    
    # Set the QGroupBox layout and show the QGroupBox
    window.setLayout(vbox)
    window.show()

    app.exec()

if __name__ == '__main__':
    main()