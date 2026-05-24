#!/usr/bin/env python
# coding: utf-8

from enum import Enum
import tkinter as tk
from tkinter import messagebox

from account_service import AccountService
from student_data_repository import StudentDataRepository
from subject_enrollment_service import SubjectEnrollmentService


class AppState(Enum):
    LOGIN = "login"
    ENROLMENT = "enrolment"
    EXIT = "exit"


# ==============================
# App — wires services, manages state
# ==============================

class GUIUniApp:
    def __init__(self, root):
        self.root = root
        self.current_state = AppState.LOGIN
        self.current_student_id = None
        self.current_frame = None

        self.student_data_repository = StudentDataRepository()
        self.account_service = AccountService(self.student_data_repository)
        self.subject_enrollment_service = SubjectEnrollmentService(self.student_data_repository)

        self.run()

    def run(self):
        if self.current_state == AppState.LOGIN:
            self._show_login()
        elif self.current_state == AppState.ENROLMENT:
            self._show_enrolment()
        elif self.current_state == AppState.EXIT:
            self.root.destroy()

    def _set_state(self, state, student_id=None):
        self.current_state = state
        self.current_student_id = student_id

        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

        self.run()

    def _show_login(self):
        self.root.title("GUIUniApp - Login")
        self.root.geometry("380x230")
        self.current_frame = LoginFrame(self.root, self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def _show_enrolment(self):
        self.root.title("GUIUniApp - Enrolment")
        self.root.geometry("530x430")
        self.current_frame = EnrolmentFrame(self.root, self, self.current_student_id)
        self.current_frame.pack(fill=tk.BOTH, expand=True)


# ==============================
# Login Frame
# ==============================

class LoginFrame(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root)
        self.app = app

        tk.Label(self, text="Student Login", font=("Arial", 16)).pack(pady=15)

        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self, width=35)
        self.email_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, width=35, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=15)
        tk.Button(self, text="Quit", command=lambda: app._set_state(AppState.EXIT)).pack()

    def login(self):
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get().strip()

        if email == "" or password == "":
            messagebox.showerror("Error", "Email and password cannot be empty")
            return

        student, error = self.app.account_service.login(email, password)

        if student is None:
            messagebox.showerror("Error", error)
            return

        messagebox.showinfo("Success", "Login successful")
        self.app._set_state(AppState.ENROLMENT, student.id)


# ==============================
# Enrolment Frame
# ==============================

class EnrolmentFrame(tk.Frame):
    def __init__(self, root, app, student_id):
        super().__init__(root)
        self.app = app
        self.student_id = student_id

        tk.Label(
            self,
            text=f"Student ID: {student_id}",
            font=("Arial", 14)
        ).pack(pady=10)

        self.subject_list = tk.Listbox(self, width=55, height=9)
        self.subject_list.pack(pady=5)

        tk.Button(
            self,
            text="Enrol Subject",
            command=self.enrol_subject
        ).pack(pady=4)

        tk.Button(
            self,
            text="Open Subject Window",
            command=self.open_subject_window
        ).pack(pady=4)

        frame = tk.Frame(self)
        frame.pack(pady=4)

        tk.Label(frame, text="Remove Subject ID:").pack(side=tk.LEFT)

        self.remove_entry = tk.Entry(frame, width=10)
        self.remove_entry.pack(side=tk.LEFT)

        tk.Button(
            frame,
            text="Remove",
            command=self.remove_subject
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self,
            text="Change Password",
            command=self.open_password_window
        ).pack(pady=5)

        tk.Button(
            self,
            text="Logout",
            command=lambda: app._set_state(AppState.LOGIN)
        ).pack()

        self.refresh_subjects()

    def refresh_subjects(self):
        self.subject_list.delete(0, tk.END)

        student = self.app.account_service.get_student(self.student_id)

        if student is None:
            self.subject_list.insert(tk.END, "Student does not exist")
            return

        if len(student.subjects) == 0:
            self.subject_list.insert(tk.END, "< Nothing to Display >")
            return

        for subject in student.subjects:
            self.subject_list.insert(tk.END, f"Subject-{subject['id']} | Mark: {subject['mark']} | Grade: {subject['grade']}")

        avg = student.average_mark()
        self.subject_list.insert(tk.END, "")
        self.subject_list.insert(tk.END, f"Average Mark: {avg:.2f}")

    def enrol_subject(self):
        subject_id, error = self.app.subject_enrollment_service.enrol_subject(self.student_id)

        if subject_id is None:
            messagebox.showerror("Error", error)
            return

        messagebox.showinfo("Success", f"Enrolled in Subject-{subject_id}")
        self.refresh_subjects()

    def remove_subject(self):
        subject_id = self.remove_entry.get().strip()

        if subject_id.isdigit():
            subject_id = subject_id.zfill(3)

        if len(subject_id) != 3 or not subject_id.isdigit():
            messagebox.showerror("Error", "Invalid subject ID")
            return

        success, error = self.app.subject_enrollment_service.remove_subject(self.student_id, subject_id)

        if not success:
            messagebox.showerror("Error", error)
            return

        messagebox.showinfo("Success", f"Subject-{subject_id} removed")
        self.refresh_subjects()

    def open_subject_window(self):
        SubjectWindow(self.app.root, self.app, self.student_id)

    def open_password_window(self):
        PasswordWindow(self.app.root, self.app, self.student_id)


# ==============================
# Subject Window (Toplevel overlay)
# ==============================

class SubjectWindow:
    def __init__(self, root, app, student_id):
        self.app = app
        self.student_id = student_id

        self.window = tk.Toplevel(root)
        self.window.title("Subject Window")
        self.window.geometry("420x260")

        self.text_box = tk.Text(self.window, width=50, height=12)
        self.text_box.pack(pady=10)

        tk.Button(
            self.window,
            text="Close",
            command=self.window.destroy
        ).pack()

        self.show_subjects()

    def show_subjects(self):
        self.text_box.delete("1.0", tk.END)

        student = self.app.account_service.get_student(self.student_id)

        if student is None:
            self.text_box.insert(tk.END, "Student does not exist")
            return

        if len(student.subjects) == 0:
            self.text_box.insert(tk.END, "< Nothing to Display >")
            return

        for subject in student.subjects:
            self.text_box.insert(tk.END, f"Subject-{subject['id']} --> mark: {subject['mark']} --> grade: {subject['grade']}\n")


# ==============================
# Password Window (Toplevel overlay)
# ==============================

class PasswordWindow:
    def __init__(self, root, app, student_id):
        self.app = app
        self.student_id = student_id

        self.window = tk.Toplevel(root)
        self.window.title("Change Password")
        self.window.geometry("330x220")

        tk.Label(
            self.window,
            text="Change Password",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(self.window, text="New Password:").pack()
        self.new_password_entry = tk.Entry(self.window, width=30, show="*")
        self.new_password_entry.pack()

        tk.Label(self.window, text="Confirm Password:").pack()
        self.confirm_password_entry = tk.Entry(self.window, width=30, show="*")
        self.confirm_password_entry.pack()

        tk.Button(
            self.window,
            text="Change",
            command=self.change_password
        ).pack(pady=15)

    def change_password(self):
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if new_password == "" or confirm_password == "":
            messagebox.showerror("Error", "Password cannot be empty")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Password does not match - try again")
            return

        success, error = self.app.account_service.change_password(self.student_id, new_password)

        if not success:
            messagebox.showerror("Error", error)
            return

        messagebox.showinfo("Success", "Password updated successfully")
        self.window.destroy()


# ==============================
# Start Program
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIUniApp(root)
    root.mainloop()
