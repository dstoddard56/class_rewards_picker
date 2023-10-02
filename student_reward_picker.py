import math
import csv
import pandas as pd
'''
each week kids can get a point each week. after each week, the number of points
are totalled and the kids are assigned a proability of winning the prize based on their point
total. the kid with the most points has the highest probability of winning the prize.
'''
file_path = "C:\Users\12078\OneDrive\Desktop\classList.xlsx"

columns_to_import = ['First', 'Teacher']

combined_data = pd.DataFrame()

sheets_excluded = ['Master List', 'Snow']

xls = pd.ExcelFile(file_path)

for sheet_name, sheet_data in xls.sheet_names:
    if sheet_name not in sheets_excluded:
        sheet_data = sheet_name
        combined_data = combined_data.append(sheet_data, ignore_index=True)

for sheet_name in xls.sheet_names:
    if sheet_name not in sheets_excluded:
        sheet_data = xls.parse(sheet_name)
        combined_data = combined_data.append(sheet_data, ignore_index=True)
    
class StudentData:
    def __init__(self, file_path, sheets_excluded=None):
        self.file_path = file_path
        self.sheets_excluded = sheets_excluded
        self.students_by_teacher = {}
        self.all_students = []

    def get_student_data(self):
        xls = pd.ExcelFile(self.file_path)
        for sheet_name in xls.sheet_names:
            if sheet_name not in self.sheets_excluded:
                sheet_data = xls.parse(sheet_name)
                for index, row, in sheet.data_iterrows():
                    name = row['First']
                    teacher = row['Teacher']
                    if teacher not in self.students_by_teacher:
                        self.students_by_teacher[teacher] = []
                    self.students_by_teacher[teacher].append(name)
                    self.all_students.append('Name:' name, 'Teacher:' teacher)
    
    def get_students_by_teacher(self):
        return self.students_by_teacher(teacher_name, [])
    
    def get_all_students(self):
        return self.all_students
    
    def sort_students_by_teacher(self):
        sorted_students = {}
        for student_info in self.all_students:
            student_name = student_info['Name']
            student_teacher = student_info['Teacher']
            if student_teacher not in sorted_students:
                sorted_students[student_teacher] = []
            sorted_students[student_teacher].append(student_name)
        return sorted_students
    
    def assign_points(self, student_name, points):
        for student_info in self.all_students:
            if student_info['Name'] == student_name:
                student_info['Points'] = points
                break

def select_classroom(data_manager):
    print("Select a classroom by entering teacher's last name:")
    for teacher in data_manager.get_students_by_teacher.keys():
        print(teacher)
    teacher_name = input()
    return teacher_name

def assign_student_points(data_manager):
    teacher_name = select_classroom(data_manager)
    students = data_manager.get_students_by_teacher(teacher_name)

    if not students:
        print("No students found for teacher: {}".format(teacher_name))
        return
    print(f'Assign points to students in {teacher_name}\'s class:')
    for student in students:
        while True:
            try:
                points = int(input(f'{student}: '))
                
                data_manager.assign_points(student, points)
                break
            except ValueError:
                print('Please enter a valid number')
