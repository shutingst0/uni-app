#!/usr/bin/env python
# coding: utf-8

# Yuhang Wang
import random

from account_service import AccountService
from constants import MAX_SUBJECTS
from database import db
from subject import Subject
from utils import average_mark, generate_subject_id, grade_from_mark, input_text, student_grade, validate_password


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

    student = AccountService(db.read_students()).register(name, email, password)
    if student is None:
        return

    db.save_student(student)
    print(f"Student {student['name']} registered successfully")
    print("Student ID:", student["id"])


def login_student():
    print("Student Sign In")

    email = input_text("Email: ").strip().lower()
    password = input_text("Password: ").strip()

    student = AccountService(db.read_students()).login(email, password)
    if student is None:
        return

    print("Student login successful")
    return student["id"]


# =========================
# Subject Enrolment System
# =========================

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


# =========================
# Main University System
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


def student_menu():
    while True:
        choice = input_text("Student System (l/r/x): ").strip().lower()

        if choice == "l":
            student_id = login_student()
            if student_id:
                subject_menu(student_id)
        elif choice == "r":
            register_student()
        elif choice == "x":
            break
        else:
            print("Invalid option")


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
