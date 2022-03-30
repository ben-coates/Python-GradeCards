def updateStudentList(students, writeablefile):
    for s in students:
        writeablefile.write(s.name + " " + s.gender + "\n")