import json
import os

DATA_FILE = "students.data"


class Database:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.create_file_if_missing()

    def create_file_if_missing(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file)

    def read_students(self):
        self.create_file_if_missing()

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

            return []

        except json.JSONDecodeError:
            print("Database file is damaged. Starting with empty data.")
            return []

    def write_students(self, students):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=2)

    def clear_students(self):
        self.write_students([])

    def find_student_by_email(self, email):
        students = self.read_students()

        for student in students:
            if student["email"].lower() == email.lower():
                return student

        return None

    def find_student_by_id(self, student_id):
        students = self.read_students()

        for student in students:
            if student["id"] == student_id:
                return student

        return None

    def save_student(self, updated_student):
        students = self.read_students()

        for i in range(len(students)):
            if students[i]["id"] == updated_student["id"]:
                students[i] = updated_student
                self.write_students(students)
                return

        students.append(updated_student)
        self.write_students(students)

    def remove_student(self, student_id):
        students = self.read_students()
        new_students = []

        found = False

        for student in students:
            if student["id"] == student_id:
                found = True
            else:
                new_students.append(student)

        if found:
            self.write_students(new_students)

        return found


db = Database()
