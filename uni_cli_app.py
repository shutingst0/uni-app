#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Yuhang Wang 
import json
import os
import random
import re


DATA_FILE = "students.data"
MAX_SUBJECTS = 4

EMAIL_RE = re.compile(r"@university\.com$", re.IGNORECASE)
PASSWORD_RE = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")


# =========================
# Model Classes
# =========================

class Subject:
    def __init__(self, subject_id, mark, grade):
        self.id = subject_id
        self.mark = mark
        self.grade = grade

    def to_dict(self):
        return {
            "id": self.id,
            "mark": self.mark,
            "grade": self.grade
        }

from student import Student

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


# =========================（Shuting Yang）
# Helper Functions
# =========================

def validate_email(email):
    return EMAIL_RE.search(email) is not None


def validate_password(password):
    return PASSWORD_RE.match(password) is not None


def generate_student_id():
    students = db.read_students()
    used_ids = []

    for student in students:
        used_ids.append(student["id"])

    while True:
        new_id = str(random.randint(1, 999999)).zfill(6)

        if new_id not in used_ids:
            return new_id


def generate_subject_id(subjects):
    used_ids = []

    for subject in subjects:
        used_ids.append(subject["id"])

    while True:
        new_id = str(random.randint(1, 999)).zfill(3)

        if new_id not in used_ids:
            return new_id


def grade_from_mark(mark):
    if mark < 50:
        return "Z"
    elif mark < 65:
        return "P"
    elif mark < 75:
        return "C"
    elif mark < 85:
        return "D"
    else:
        return "HD"


def average_mark(student):
    subjects = student["subjects"]

    if len(subjects) == 0:
        return 0.0

    total = 0

    for subject in subjects:
        total += subject["mark"]

    return total / len(subjects)


def student_grade(student):
    return grade_from_mark(average_mark(student))


def input_text(message):
    try:
        return input(message)
    except EOFError:
        return ""


# =========================
# Student Register / Login
# =========================

def register_student():
    print("Student Sign Up")

    name = input_text("Name: ").strip()
    email = input_text("Email: ").strip().lower()
    password = input_text("Password: ").strip()

    if name == "":
        print("Name cannot be empty")
        return

    if not validate_email(email):
        print("Incorrect email format")
        return

    if not validate_password(password):
        print("Incorrect password format")
        return

    existing_student = db.find_student_by_email(email)

    if existing_student is not None:
        print("Student already exists")
        return

    student_id = generate_student_id()

    new_student = Student(
        student_id,
        name,
        email,
        password
    ).to_dict()

    db.save_student(new_student)

    print("Student registered successfully")
    print("Student ID:", student_id)


def login_student():
    print("Student Sign In")

    email = input_text("Email: ").strip().lower()
    password = input_text("Password: ").strip()

    if not validate_email(email):
        print("Incorrect email format")
        return

    if not validate_password(password):
        print("Incorrect password format")
        return

    student = db.find_student_by_email(email)

    if student is None:
        print("Student does not exist")
        return

    if student["password"] != password:
        print("Incorrect password")
        return

    print("Student login successful")
    subject_menu(student["id"])


# =========================
# Subject Enrolment System（Ming Sun ）
# =========================

def subject_menu(student_id):
    while True:
        choice = input_text("Student Course Menu (c/e/r/s/x): ").strip().lower()

        if choice == "c":
            change_password(student_id)
        elif choice == "e":
            enrol_subject(student_id)
        elif choice == "r":
            remove_subject(student_id)
        elif choice == "s":
            show_subjects(student_id)
        elif choice == "x":
            break
        else:
            print("Invalid option")


def change_password(student_id):
    print("Updating Password")

    student = db.find_student_by_id(student_id)

    if student is None:
        print("Student does not exist")
        return

    new_password = input_text("New Password: ").strip()
    confirm_password = input_text("Confirm Password: ").strip()

    if new_password != confirm_password:
        print("Password does not match - try again")
        return

    if not validate_password(new_password):
        print("Incorrect password format")
        return

    student["password"] = new_password
    db.save_student(student)

    print("Password updated successfully")


def enrol_subject(student_id):
    student = db.find_student_by_id(student_id)

    if student is None:
        print("Student does not exist")
        return

    subjects = student["subjects"]

    if len(subjects) >= MAX_SUBJECTS:
        print("Students are allowed to enrol in 4 subjects only")
        return

    subject_id = generate_subject_id(subjects)
    mark = random.randint(25, 100)
    grade = grade_from_mark(mark)

    subject = Subject(subject_id, mark, grade).to_dict()
    subjects.append(subject)

    db.save_student(student)

    print("Enrolling in Subject-" + subject_id)
    print("You are now enrolled in", len(subjects), "out of 4 subjects")


def remove_subject(student_id):
    student = db.find_student_by_id(student_id)

    if student is None:
        print("Student does not exist")
        return

    subject_id = input_text("Remove Subject by ID: ").strip()

    if subject_id.isdigit():
        subject_id = subject_id.zfill(3)

    if len(subject_id) != 3 or not subject_id.isdigit():
        print("Invalid subject ID")
        return

    subjects = student["subjects"]
    new_subjects = []

    found = False

    for subject in subjects:
        if subject["id"] == subject_id:
            found = True
        else:
            new_subjects.append(subject)

    if not found:
        print("Subject does not exist")
        return

    student["subjects"] = new_subjects
    db.save_student(student)

    print("Dropping Subject-" + subject_id)


def show_subjects(student_id):
    student = db.find_student_by_id(student_id)

    if student is None:
        print("Student does not exist")
        return

    subjects = student["subjects"]

    print("Showing", len(subjects), "subjects")

    if len(subjects) == 0:
        print("< Nothing to Display >")
        return

    for subject in subjects:
        print(
            "Subject-" + subject["id"],
            "--> mark:",
            subject["mark"],
            "--> grade:",
            subject["grade"]
        )

    print("Average Mark:", format(average_mark(student), ".2f"))


# =========================
# Admin System
# =========================

def admin_menu():
    while True:
        choice = input_text("Admin System (c/g/p/r/s/x): ").strip().lower()

        if choice == "c":
            clear_database()
        elif choice == "g":
            group_students()
        elif choice == "p":
            partition_students()
        elif choice == "r":
            remove_student()
        elif choice == "s":
            show_all_students()
        elif choice == "x":
            break
        else:
            print("Invalid option")


def show_all_students():
    students = db.read_students()

    print("Student List")

    if len(students) == 0:
        print("< Nothing to Display >")
        return

    for student in students:
        print(
            student["name"],
            "::",
            student["id"],
            "--> Email:",
            student["email"]
        )


def group_students():
    students = db.read_students()

    print("Grade Grouping")

    if len(students) == 0:
        print("< Nothing to Display >")
        return

    groups = {
        "HD": [],
        "D": [],
        "C": [],
        "P": [],
        "Z": []
    }

    for student in students:
        grade = student_grade(student)
        groups[grade].append(student)

    for grade in groups:
        if len(groups[grade]) > 0:
            print(grade, "-->", end=" ")

            for student in groups[grade]:
                avg = average_mark(student)
                print(
                    "[" + student["name"],
                    "::",
                    student["id"],
                    "--> GRADE:",
                    grade,
                    "--> MARK:",
                    format(avg, ".2f") + "]",
                    end=" "
                )

            print()


def partition_students():
    students = db.read_students()

    print("PASS/FAIL Partition")

    pass_students = []
    fail_students = []

    for student in students:
        subjects = student["subjects"]
        avg = average_mark(student)

        if len(subjects) == MAX_SUBJECTS and avg >= 50:
            pass_students.append(student)
        else:
            fail_students.append(student)

    print("FAIL -->", format_student_list(fail_students))
    print("PASS -->", format_student_list(pass_students))


def format_student_list(students):
    if len(students) == 0:
        return "[]"

    text = "["

    for student in students:
        grade = student_grade(student)
        avg = average_mark(student)

        text += (
            student["name"]
            + " :: "
            + student["id"]
            + " --> GRADE: "
            + grade
            + " --> MARK: "
            + format(avg, ".2f")
            + ", "
        )

    text = text.rstrip(", ")
    text += "]"

    return text


def remove_student():
    student_id = input_text("Remove by ID: ").strip()

    if len(student_id) != 6 or not student_id.isdigit():
        print("Invalid student ID")
        return

    removed = db.remove_student(student_id)

    if removed:
        print("Removing Student", student_id, "Account")
    else:
        print("Student", student_id, "does not exist")


def clear_database():
    print("Clearing students database")

    answer = input_text("Are you sure you want to clear the database (Y)ES/(N)O: ")
    answer = answer.strip().lower()

    if answer == "y" or answer == "yes":
        db.clear_students()
        print("Students data cleared")
    else:
        print("Clear cancelled")


# =========================（JIN JIE DENG）
# Main University System
# =========================

def student_menu():
    while True:
        choice = input_text("Student System (l/r/x): ").strip().lower()

        if choice == "l":
            login_student()
        elif choice == "r":
            register_student()
        elif choice == "x":
            break
        else:
            print("Invalid option")


def university_menu():
    while True:
        choice = input_text("University System: (A)dmin, (S)tudent, or X: ")
        choice = choice.strip().lower()

        if choice == "a":
            admin_menu()
        elif choice == "s":
            student_menu()
        elif choice == "x":
            print("Thank You")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    university_menu()

