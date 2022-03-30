import re
import io
from student import Student

def parseReport(progressReport):
    studentList = []
    studentData = []
    progressReportLines = io.StringIO(progressReport)
    
    for line in progressReportLines.readlines():
        # Remove end of line characters. Split lines on tabs and colons
        newLine = line.replace("\n", "")
        newLine = re.split(r"\t|:", newLine)
        
        # Remove whitespace on both ends of the data points
        for i, item in enumerate(newLine):
            newLine[i] = item.lstrip().rstrip()

        # Check if the line is Progress Report
        # If so, reset Student Record
        if "Progress Report" in newLine:
            currentStudent = { 'classes': [] }

        # Check if length of line is 2
        # If so, update record with key of first item and value of second item
        elif (len(newLine) == 2):
            currentStudent.update({newLine[0].replace(" ","").lower(): newLine[1]})
        # Check if length of line is 4 and GPA is not included in the first item
        # If so, update the record with key of the first item and key:value pairs of the remaining items
        elif (len(newLine) == 4 and not "GPA" in newLine[0] and not "Class" in newLine[0]):
            currentStudent.get('classes').append({
                'classname': newLine[0],
                'credits': newLine[1],
                'lettergrade': newLine[2][0:newLine[2].find(" ")],
                'percentage': newLine[2][newLine[2].find("(") + 1:newLine[2].find("%)")],
                'effort': int(newLine[3])
            })
        # Check if length of line is 4 and GPA is included in the first item
        # If so, update the roced with 2 key:value pairs of the first:second and third:fourth
        elif (len(newLine) == 4 and "GPA" in newLine[0]):
            currentStudent.update({'gpa': float(newLine[1])})
            currentStudent.update({'units': float(newLine[3])})

            # GPA will be the last line so add student to data array
            studentData.append(currentStudent)

    for i in studentData:
        newStudent = Student(
            i.get('student'),
            i.get('id'),
            i.get('gradelevel'),
            i.get('date'),
            i.get('term'),
            i.get('gpa'),
            i.get('units'),
            i.get('classes')
        )
        studentList.append(newStudent)

    return studentList