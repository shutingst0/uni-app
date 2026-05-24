import random
import re

from printer import Printer
from student import Student
from utils import pad_number


class AccountService:
    def __init__(self, student_data_repository):
        self.student_data_repository = student_data_repository

    def validate(self, email, password):
        valid_email = bool(re.match(r"[^@]+@university\.com$", email))
        valid_password = bool(re.match(r"[A-Z][a-zA-Z]{4,}\d{3,}", password))

        if valid_password is False or valid_email is False:
            Printer.error("Incorrect email or password format")
            return False

        Printer.warn("email and password format acceptable")
        return True

    def _generate_unique_student_id(self):
        existing_ids = []
        for student in self.student_data_repository.read_students():
            existing_ids.append(student.id)

        while True:
            new_id = pad_number(random.randint(0, 999999), 6)
            if new_id not in existing_ids:
                return new_id

    def register(self, name, email, password):
        is_valid = self.validate(email, password)
        if not is_valid:
            return

        existing_student = self.student_data_repository.find_student_by_email(email)
        if existing_student:
            Printer.error(f"Student with email {email} already exist")
            return

        student_id = self._generate_unique_student_id()
        student = Student(student_id, name, email, password)
        self.student_data_repository.create_student(student)
        Printer.success(f"Signed up student {student.name}")
        return student

    def change_password(self, student_id, new_password):
        student = self.student_data_repository.find_student_by_id(student_id)
        if student is None:
            Printer.error("Student does not exist")
            return False

        is_valid = self.validate(student.email, new_password)
        if not is_valid:
            return False

        student.password = new_password
        self.student_data_repository.update_student(student)
        Printer.success("Password updated successfully")
        return True

    def login(self, email, password):
        is_valid = self.validate(email, password)
        if not is_valid:
            return

        student = self.student_data_repository.find_student_by_email(email)
        is_correct_password = student and student.password == password
        if is_correct_password:
            Printer.success("Login successful")
            return student

        Printer.error("Student does not exist")
        return None
