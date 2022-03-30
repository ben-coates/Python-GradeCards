# Python Library file imports
from msilib.schema import ListBox
from tkinter import messagebox, filedialog
from tkinter import *
from openpyxl import Workbook

# Program file imports
from deansreport import runDeansReport
from formatGradecards import runGradeCards
from parseReport import parseReport
from studentList import updateStudentList

# Global variable
students = []

# parse the data and visualize it in editable fields
def visualizeData(frame, text):

    # Grab the text from the report excluding the first line until the end
    progressReport = text.get('1.0','end')

    # Set student variable to the list returned from the students function
    students = parseReport(progressReport)

    studentList = open('students.txt', 'w')
    updateStudentList(students, studentList)
    studentList.close()
    # name = Label(frame, text = "Name")
    # name.grid(row = 0, column = 0)
    # id = Label(frame, text = "ID")
    # id.grid(row = 0, column = 1)
    # gradelevel = Label(frame, text = "Grade")
    # gradelevel.grid(row = 0, column = 2)
    # gpa = Label(frame, text = "GPA")
    # gpa.grid(row = 0, column = 3)
    # eligibility = Label(frame, text = "Eligibility")
    # eligibility.grid(row = 0, column = 4)
    # effort = Label(frame, text = "Effort")
    # effort.grid(row = 0, column = 5)

    # for index, s in enumerate(students):
    #     name = Label(frame, text = s.name)
    #     name.grid(row = index + 1, column = 0, sticky=W)
    #     id = Label(frame, text = s.id)
    #     id.grid(row = index + 1, column = 1)
    #     gradelevel = Label(frame, text = s.gradelevel)
    #     gradelevel.grid(row = index + 1, column = 2)
    #     gpa = Label(frame, text = s.gpa)
    #     gpa.grid(row = index + 1, column = 3)
    #     eligibility = Label(frame, text = s.eligibility)
    #     eligibility.grid(row = index + 1, column = 4)
    #     effort = Label(frame, text = s.effort)
    #     effort.grid(row = index + 1, column = 5)

def saveReport(root, students):
    # Prompt user to save file and request a save destination
    messagebox.showinfo("Save Report", "Please select or create a file to save the gradecard report.") 
    gradecardsReport = filedialog.asksaveasfilename(title = "Select Location to Save Gradecards", defaultextension=".xlsx", filetypes=(("Excel File", "*.xlsx"),))
    
    # Create a workbook, run the deans report, run the gradecards, save the file
    workbook = Workbook()
    runDeansReport(students, workbook)
    runGradeCards(students, workbook)
    workbook.save(filename=gradecardsReport)

    # Report to user that the report has been saved
    messagebox.showinfo("Report Save", "Report has been saved to " + gradecardsReport) 
    root.destroy()

def processTextFile(text):
    progressReport = filedialog.askopenfilename(title = "Select Progress Report", defaultextension=".txt", filetypes=(("Text File", "*.txt"),))
    for index, line in enumerate(open(progressReport).readlines()):
        text.insert(float(index), line)

def main():
    # Create the Tk() root element and give it a title, starting dimensons and icon
    root = Tk()
    root.title('Oakdale Gradecards')
    # root.geometry(f'{screen_width - 200}x{screen_height - 200}+100+50')
    # root.iconbitmap('gradecards.ico')

    text = Text(root, height=20)
    text.pack(padx=30, pady=30)

    # dataScroll.config(command=text.yview)

    listbox = Listbox(root)
    l1 = Label(listbox, text = "Hello")
    listbox.insert(1, l1)
    listbox.pack()

    dataFrame = Frame(root)
    dataFrame.pack()

    button = Button(root, text="Load Data from Text File", command=lambda:processTextFile(text))
    button.pack(padx=10, pady=10)
    button = Button(root, text="Process Data", command=lambda:visualizeData(dataFrame, text))
    button.pack(padx=10, pady=10)
    button = Button(root, text="Run Report", command=lambda:saveReport(root, students))
    button.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()