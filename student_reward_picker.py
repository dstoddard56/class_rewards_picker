import pandas as pd
import random

class StudentData:
    def __init__(self, file_path, sheets_excluded=None):
        self.file_path = file_path
        self.sheets_excluded = sheets_excluded or []
        self.students_by_teacher = {}
        self.all_students = []

    def get_student_data(self):
        xls = pd.ExcelFile(self.file_path)
        for sheet_name in xls.sheet_names:
            if sheet_name not in self.sheets_excluded:
                sheet_data = xls.parse(sheet_name)
                for index, row in sheet_data.iterrows():
                    name = row['First']
                    teacher = row['Teacher']
                    if teacher not in self.students_by_teacher:
                        self.students_by_teacher[teacher] = []
                    self.students_by_teacher[teacher].append(name)
                    self.all_students.append({'Name': name, 'Teacher': teacher, 'Points': 0, 'Probability': 0})

    def get_students_by_teacher(self, teacher_name):
        return self.students_by_teacher.get(teacher_name, [])

    def get_all_students(self):
        return self.all_students

    def assign_points(self, student_name, points):
        for student_info in self.all_students:
            if student_info['Name'] == student_name:
                student_info['Points'] = points
                break

    def calculate_probabilities(self):
        max_points = max(student['Points'] for student in self.all_students)
        for student_info in self.all_students:
            student_points = student_info['Points']
            
            if max_points > 0:
                # Calculate a random factor between 0.9 and 1.1 to introduce randomness
                random_factor = random.uniform(0.1, 0.9)
                
                # Calculate the probability with randomness
                student_info['Probability'] = (student_points / max_points) * random_factor
            else:
                student_info['Probability'] = 0

    def select_winner(self):
        self.calculate_probabilities()
        
        # Create a list of students with their probabilities repeated for randomness
        weighted_students = []
        for student_info in self.all_students:
            probability = student_info['Probability']
            weighted_students.extend([student_info['Name']] * int(probability * 100))  # Multiply by 100 for better randomness
        
        # Use random choice to select a winner
        winner = random.choice(weighted_students)
        
        return winner

def select_classroom(data_manager):
    print("Select a classroom by entering teacher's last name:")
    for teacher_name in data_manager.students_by_teacher.keys():
        print(teacher_name)
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
            except ValueError:
                print('Please enter a valid number')

if __name__ == "__main__":
    file_path = r"C:\Users\12078\OneDrive\Desktop\classList.xlsx"
    data_manager = StudentData(file_path, sheets_excluded=['Master List', 'Snow'])
    data_manager.get_student_data()

    assign_student_points(data_manager)

    # Calculate probabilities and select a winner
    data_manager.calculate_probabilities()
    winner = data_manager.select_winner()
    
    # Print the winner
    print(f"The winner is: {winner}")
    
    '''
    # Print student probabilities of winning for the selected classroom after randomness is applied
    selected_classroom = select_classroom(data_manager)
    print(f"Student Probabilities of Winning in {selected_classroom}'s Class after Randomness:")
    for student_info in data_manager.get_all_students():
        if student_info['Teacher'] == selected_classroom:
            student_name = student_info['Name']
            student_probability = student_info['Probability']
            print(f"Student: {student_name}, Probability: {student_probability:.2f}")
    '''
