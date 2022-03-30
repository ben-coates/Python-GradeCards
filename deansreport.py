from openpyxl.styles import Font, Alignment, PatternFill

def headerCell(sheet, cell, text, width, color):
    sheet[cell] = text
    sheet[cell].alignment = Alignment(horizontal='center', vertical='center')
    sheet[cell].fill = PatternFill("solid", start_color="008000")
    sheet[cell].font = Font(color="FFFFFF")
    sheet.column_dimensions[cell[0]].width = width

def runDeansReport(report, workbook):
    sort_order = ['Honor Roll', 'Eligible', 'Limited', 'Ineligible']
    report = sorted(report, key=lambda s: s.name)
    report = sorted(report, key=lambda s: s.gpa, reverse=True)
    report = sorted(report, key=lambda s: sort_order.index(s.eligibility))

    # Create Worksheet
    sheet = workbook.create_sheet(title="Deans Report")

    # Create and Format Header Rows
    headerCell(sheet, "A1", "Student Name", 40, "008000")
    headerCell(sheet, "B1", "GPA", 8, "008000")
    headerCell(sheet, "C1", "Eligibility", 15, "008000")

    # Add Report Data to Worksheet
    for index, student in enumerate(report):
        sheet["A" + str((index + 2))] = student.name
        sheet["B" + str((index + 2))] = student.gpa
        sheet["C" + str((index + 2))] = student.eligibility

    for index, row in enumerate(sheet.rows):
        if index % 2 != 0:
            for cell in row:
                cell.fill = PatternFill("solid", start_color="EFEFEF")
        sheet.row_dimensions[index + 1].height = 12
        cell_B = row[1]
        cell_B.alignment = Alignment(horizontal='center')
        cell_C = row[2]
        cell_C.alignment = Alignment(horizontal='center')
    
    sheet.print_area = 'A1:C' + str(len(report) + 1)

