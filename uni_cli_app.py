#!/usr/bin/env python
# coding: utf-8

from enum import Enum

from account_service import AccountService
from admin_service import AdminService
from student_data_repository import StudentDataRepository
from subject_enrollment_service import SubjectEnrollmentService
from utils import input_text


class AppState(Enum):
    UNIVERSITY = "university"
    STUDENT = "student"
    SUBJECT = "subject"
    ADMIN = "admin"
    EXIT = "exit"


class SubjectMenu:
    def __init__(self, account_service, subject_enrollment_service, student_data_repository):
        self.account_service = account_service
        self.subject_enrollment_service = subject_enrollment_service
        self.student_data_repository = student_data_repository

    def run(self, student_id, on_exit):
        while True:
            choice = input_text("Student Course Menu (c/e/r/s/x): ").strip().lower()

            if choice == "c":
                self._change_password(student_id)
            elif choice == "e":
                self._enrol_subject(student_id)
            elif choice == "r":
                self._remove_subject(student_id)
            elif choice == "s":
                self._show_subjects(student_id)
            elif choice == "x":
                on_exit()
                break
            else:
                print("Invalid option")

    def _change_password(self, student_id):
        print("Updating Password")

        new_password = input_text("New Password: ").strip()
        confirm_password = input_text("Confirm Password: ").strip()

        if new_password != confirm_password:
            print("Password does not match - try again")
            return

        self.account_service.change_password(student_id, new_password)

    def _enrol_subject(self, student_id):
        self.subject_enrollment_service.enrol_subject(student_id)

    def _remove_subject(self, student_id):
        subject_id = input_text("Remove Subject by ID: ").strip()

        if subject_id.isdigit():
            subject_id = subject_id.zfill(3)

        if len(subject_id) != 3 or not subject_id.isdigit():
            print("Invalid subject ID")
            return

        self.subject_enrollment_service.remove_subject(student_id, subject_id)

    def _show_subjects(self, student_id):
        student = self.student_data_repository.find_student_by_id(student_id)

        if student is None:
            print("Student does not exist")
            return

        print("Showing", len(student.subjects), "subjects")

        if len(student.subjects) == 0:
            print("< Nothing to Display >")
            return

        print(student)


class StudentMenu:
    def __init__(self, account_service):
        self.account_service = account_service

    def run(self, on_exit, on_login):
        while True:
            choice = input_text("Student System (l/r/x): ").strip().lower()

            if choice == "l":
                student_id = self._login()
                if student_id:
                    on_login(student_id)
                    break
            elif choice == "r":
                self._register()
            elif choice == "x":
                on_exit()
                break
            else:
                print("Invalid option")

    def _register(self):
        print("Student Sign Up")

        name = input_text("Name: ").strip()
        email = input_text("Email: ").strip().lower()
        password = input_text("Password: ").strip()

        if name == "":
            print("Name cannot be empty")
            return

        student = self.account_service.register(name, email, password)
        if student is None:
            return

        print(f"Student {student.name} registered successfully")
        print("Student ID:", student.id)

    def _login(self):
        print("Student Sign In")

        email = input_text("Email: ").strip().lower()
        password = input_text("Password: ").strip()

        student = self.account_service.login(email, password)
        if student is None:
            return None

        print("Student login successful")
        return student.id


class AdminMenu:
    def __init__(self, admin_service):
        self.admin_service = admin_service

    def run(self, on_exit):
        while True:
            choice = input_text("Admin System (c/g/p/r/s/x): ").strip().lower()

            if choice == "c":
                self._clear_database()
            elif choice == "g":
                self._group_students()
            elif choice == "p":
                self._partition_students()
            elif choice == "r":
                self._remove_student()
            elif choice == "s":
                self._show_all_students()
            elif choice == "x":
                on_exit()
                break
            else:
                print("Invalid option")

    def _show_all_students(self):
        students = self.admin_service.get_all_students()

        print("Student List")

        if len(students) == 0:
            print("< Nothing to Display >")
            return

        for student in students:
            print(student)

    def _group_students(self):
        groups = self.admin_service.group_students()

        print("Grade Grouping")

        all_empty = True
        for grade in groups:
            if len(groups[grade]) > 0:
                all_empty = False
                break

        if all_empty:
            print("< Nothing to Display >")
            return

        for grade in groups:
            if len(groups[grade]) > 0:
                print(grade, "-->", end=" ")

                for student in groups[grade]:
                    result = student.get_result()
                    print(
                        "[" + student.name,
                        "::",
                        student.id,
                        "--> GRADE:",
                        result["grade_average"],
                        "--> MARK:",
                        format(result["mark_average"], ".2f") + "]",
                        end=" "
                    )

                print()

    def _partition_students(self):
        pass_students, fail_students = self.admin_service.partition_students()

        print("PASS/FAIL Partition")
        print("FAIL -->", self._format_student_list(fail_students))
        print("PASS -->", self._format_student_list(pass_students))

    def _format_student_list(self, students):
        if len(students) == 0:
            return "[]"

        text = "["

        for student in students:
            result = student.get_result()
            text += (
                student.name
                + " :: "
                + student.id
                + " --> GRADE: "
                + result["grade_average"]
                + " --> MARK: "
                + format(result["mark_average"], ".2f")
                + ", "
            )

        text = text.rstrip(", ")
        text += "]"

        return text

    def _remove_student(self):
        student_id = input_text("Remove by ID: ").strip()

        if len(student_id) != 6 or not student_id.isdigit():
            print("Invalid student ID")
            return

        self.admin_service.remove_student(student_id)

    def _clear_database(self):
        print("Clearing students database")

        answer = input_text("Are you sure you want to clear the database (Y)ES/(N)O: ").strip().lower()

        if answer == "y" or answer == "yes":
            self.admin_service.clear_students()
        else:
            print("Clear cancelled")


class UniCLIApp:
    def __init__(self):
        student_data_repository = StudentDataRepository()
        account_service = AccountService(student_data_repository)
        subject_enrollment_service = SubjectEnrollmentService(student_data_repository)
        admin_service = AdminService(student_data_repository)

        self.subject_menu = SubjectMenu(account_service, subject_enrollment_service, student_data_repository)
        self.student_menu = StudentMenu(account_service)
        self.admin_menu = AdminMenu(admin_service)

        self.current_state = AppState.UNIVERSITY
        self.current_student_id = None

    def run(self):
        while self.current_state != AppState.EXIT:
            if self.current_state == AppState.UNIVERSITY:
                self._run_university_menu()
            elif self.current_state == AppState.STUDENT:
                self._run_student_menu()
            elif self.current_state == AppState.SUBJECT:
                self._run_subject_menu()
            elif self.current_state == AppState.ADMIN:
                self._run_admin_menu()

    def _run_university_menu(self):
        choice = input_text("University System: (A)dmin, (S)tudent, or X: ").strip().lower()

        if choice == "a":
            self.current_state = AppState.ADMIN
        elif choice == "s":
            self.current_state = AppState.STUDENT
        elif choice == "x":
            print("Thank You")
            self.current_state = AppState.EXIT
        else:
            print("Invalid option")

    def _run_student_menu(self):
        self.student_menu.run(
            on_exit=lambda: self._set_state(AppState.UNIVERSITY),
            on_login=lambda student_id: self._set_state(AppState.SUBJECT, student_id)
        )

    def _run_subject_menu(self):
        self.subject_menu.run(
            self.current_student_id,
            on_exit=lambda: self._set_state(AppState.STUDENT)
        )

    def _run_admin_menu(self):
        self.admin_menu.run(
            on_exit=lambda: self._set_state(AppState.UNIVERSITY)
        )

    def _set_state(self, state, student_id=None):
        self.current_state = state
        self.current_student_id = student_id


if __name__ == "__main__":
    UniCLIApp().run()
