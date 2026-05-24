import tkinter as tk

# messagebox is used to show popup messages
from tkinter import messagebox

# random is used to create random marks
import random

# import useful things from the CLI file
from uni_cli_app import (
    db,
    AccountService,
    grade_from_mark,
    generate_subject_id,
    Subject,
    MAX_SUBJECTS,
    average_mark
)


# ==============================
# GUI Helper Functions
# These functions invoke GUI logic
# ==============================

def get_account_service():
    students = db.read_students()
    return AccountService(students)


def find_student(student_id):
    # find student by id
    return db.find_student_by_id(student_id)


def format_subject_for_list(subject):
    # format subject for listbox
    return (
        "Subject-" + subject["id"]
        + " | Mark: " + str(subject["mark"])
        + " | Grade: " + subject["grade"]
    )


def format_subject_for_text(subject):
    # format subject for text box
    return (
        "Subject-" + subject["id"]
        + " --> mark: " + str(subject["mark"])
        + " --> grade: " + subject["grade"]
        + "\n"
    )


def check_login(email, password):
    # check empty fields
    if email == "" or password == "":
        return False, "Email and password cannot be empty", None

    account_service = get_account_service()

    student = account_service.login(email, password)

    if student is None:
        return False, "Student does not exist or password is incorrect", None

    return True, "Login successful", student


def enrol_student_subject(student_id):
    # get student
    student = find_student(student_id)

    if student is None:
        return False, "Student does not exist", None

    subjects = student["subjects"]

    # check subject limit
    if len(subjects) >= MAX_SUBJECTS:
        return False, "Students can enrol in a maximum of 4 subjects only", None

    # make new subject
    subject_id = generate_subject_id(subjects)
    mark = random.randint(25, 100)
    grade = grade_from_mark(mark)

    new_subject = Subject(subject_id, mark, grade).to_dict()

    # add subject
    subjects.append(new_subject)

    # save student
    db.save_student(student)

    return True, "Enrolled in Subject-" + subject_id, new_subject


def remove_student_subject(student_id, subject_id):
    # make id like 007
    if subject_id.isdigit():
        subject_id = subject_id.zfill(3)

    # check id format
    if len(subject_id) != 3 or not subject_id.isdigit():
        return False, "Invalid subject ID"

    # get student
    student = find_student(student_id)

    if student is None:
        return False, "Student does not exist"

    old_subjects = student["subjects"]
    new_subjects = []
    found = False

    # copy all subjects except the removed one
    for subject in old_subjects:
        if subject["id"] == subject_id:
            found = True
        else:
            new_subjects.append(subject)

    # if subject was not found
    if found == False:
        return False, "Subject does not exist"

    # save new subject list
    student["subjects"] = new_subjects
    db.save_student(student)

    return True, "Subject removed"


def update_student_password(student_id, new_password, confirm_password):
    # check empty
    if new_password == "" or confirm_password == "":
        return False, "Password cannot be empty"

    # check same password
    if new_password != confirm_password:
        return False, "Password does not match - try again"

    # use AccountService to validate password format
    account_service = get_account_service()

    # AccountService.validate needs both email and password,
    # so here we pass a valid dummy email and only use it to check password format.
    is_valid = account_service.validate("test@university.com", new_password)

    if is_valid is not True:
        return False, "Incorrect password format"

    # find student
    student = find_student(student_id)

    if student is None:
        return False, "Student does not exist"

    # update password
    student["password"] = new_password

    # save data
    db.save_student(student)

    return True, "Password updated successfully"


# ==============================
# Main Login Window
# ==============================

class GUIUniApp:
    def __init__(self, root):
        # root is the main window
        self.root = root
        self.root.title("GUIUniApp - Login")
        self.root.geometry("380x230")

        # create title
        tk.Label(root, text="Student Login", font=("Arial", 16)).pack(pady=15)

        # email input
        tk.Label(root, text="Email:").pack()
        self.email_entry = tk.Entry(root, width=35)
        self.email_entry.pack()

        # password input
        tk.Label(root, text="Password:").pack()
        self.password_entry = tk.Entry(root, width=35, show="*")
        self.password_entry.pack()

        # login button
        tk.Button(root, text="Login", command=self.login).pack(pady=15)

        # quit button
        tk.Button(root, text="Quit", command=root.destroy).pack()

    def login(self):
        # get input from text boxes
        email = self.email_entry.get().strip().lower()
        password = self.password_entry.get().strip()

        success, message, student = check_login(email, password)

        if not success:
            messagebox.showerror("Error", message)
            return

        # login success
        messagebox.showinfo("Success", message)

        # open enrolment window
        EnrolmentWindow(self.root, student["id"])


# ==============================
# Enrolment Window
# ==============================

class EnrolmentWindow:
    def __init__(self, root, student_id):
        # save student id
        self.student_id = student_id

        # create a new window
        self.window = tk.Toplevel(root)
        self.window.title("Enrolment Window")
        self.window.geometry("530x430")

        # show student id
        tk.Label(
            self.window,
            text="Student ID: " + student_id,
            font=("Arial", 14)
        ).pack(pady=10)

        # listbox shows subjects
        self.subject_list = tk.Listbox(self.window, width=55, height=9)
        self.subject_list.pack(pady=5)

        # enrol button
        tk.Button(
            self.window,
            text="Enrol Subject",
            command=self.enrol_subject
        ).pack(pady=4)

        # subject window button
        tk.Button(
            self.window,
            text="Open Subject Window",
            command=self.open_subject_window
        ).pack(pady=4)

        # remove subject area
        frame = tk.Frame(self.window)
        frame.pack(pady=4)

        tk.Label(frame, text="Remove Subject ID:").pack(side=tk.LEFT)

        self.remove_entry = tk.Entry(frame, width=10)
        self.remove_entry.pack(side=tk.LEFT)

        tk.Button(
            frame,
            text="Remove",
            command=self.remove_subject
        ).pack(side=tk.LEFT, padx=5)

        # password button
        tk.Button(
            self.window,
            text="Change Password",
            command=self.open_password_window
        ).pack(pady=5)

        # load subjects when window opens
        self.refresh_subjects()

    def get_student(self):
        # find student by id
        return find_student(self.student_id)

    def refresh_subjects(self):
        # clear listbox
        self.subject_list.delete(0, tk.END)

        # get student
        student = self.get_student()

        if student is None:
            self.subject_list.insert(tk.END, "Student does not exist")
            return

        subjects = student["subjects"]

        # if no subject
        if len(subjects) == 0:
            self.subject_list.insert(tk.END, "< Nothing to Display >")
            return

        # show subjects one by one
        for subject in subjects:
            self.subject_list.insert(tk.END, format_subject_for_list(subject))

        # show average mark
        avg = average_mark(student)
        self.subject_list.insert(tk.END, "")
        self.subject_list.insert(tk.END, "Average Mark: " + format(avg, ".2f"))

    def enrol_subject(self):
        success, message, subject = enrol_student_subject(self.student_id)

        if not success:
            messagebox.showerror("Exception Window", message)
            return

        # show message
        messagebox.showinfo("Success", message)

        # refresh list
        self.refresh_subjects()

    def remove_subject(self):
        # get subject id from input
        subject_id = self.remove_entry.get().strip()

        success, message = remove_student_subject(self.student_id, subject_id)

        if not success:
            messagebox.showerror("Error", message)
            return

        messagebox.showinfo("Success", message)

        # refresh listbox
        self.refresh_subjects()

    def open_subject_window(self):
        # open another window to show subjects
        SubjectWindow(self.window, self.student_id)

    def open_password_window(self):
        # open password change window
        PasswordWindow(self.window, self.student_id)


# ==============================
# Subject Window
# ==============================

class SubjectWindow:
    def __init__(self, root, student_id):
        self.student_id = student_id

        # create new window
        self.window = tk.Toplevel(root)
        self.window.title("Subject Window")
        self.window.geometry("420x260")

        # text box to show subjects
        self.text_box = tk.Text(self.window, width=50, height=12)
        self.text_box.pack(pady=10)

        # close button
        tk.Button(
            self.window,
            text="Close",
            command=self.window.destroy
        ).pack()

        # show subjects
        self.show_subjects()

    def show_subjects(self):
        # clear text box
        self.text_box.delete("1.0", tk.END)

        # get student
        student = find_student(self.student_id)

        if student is None:
            self.text_box.insert(tk.END, "Student does not exist")
            return

        subjects = student["subjects"]

        if len(subjects) == 0:
            self.text_box.insert(tk.END, "< Nothing to Display >")
            return

        # print every subject
        for subject in subjects:
            self.text_box.insert(tk.END, format_subject_for_text(subject))


# ==============================
# Password Window
# ==============================

class PasswordWindow:
    def __init__(self, root, student_id):
        self.student_id = student_id

        # create new window
        self.window = tk.Toplevel(root)
        self.window.title("Change Password")
        self.window.geometry("330x220")

        # title
        tk.Label(
            self.window,
            text="Change Password",
            font=("Arial", 14)
        ).pack(pady=10)

        # new password input
        tk.Label(self.window, text="New Password:").pack()
        self.new_password_entry = tk.Entry(self.window, width=30, show="*")
        self.new_password_entry.pack()

        # confirm password input
        tk.Label(self.window, text="Confirm Password:").pack()
        self.confirm_password_entry = tk.Entry(self.window, width=30, show="*")
        self.confirm_password_entry.pack()

        # change button
        tk.Button(
            self.window,
            text="Change",
            command=self.change_password
        ).pack(pady=15)

    def change_password(self):
        # get passwords
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        success, message = update_student_password(
            self.student_id,
            new_password,
            confirm_password
        )

        if not success:
            if message == "Password does not match - try again":
                messagebox.showerror("Exception Window", message)
            else:
                messagebox.showerror("Error", message)
            return

        # show success
        messagebox.showinfo("Success", message)

        # close password window
        self.window.destroy()


# ==============================
# Start Program
# ==============================

# this part only runs when this file is run directly
if __name__ == "__main__":
    # make main window
    root = tk.Tk()

    # start GUI app
    app = GUIUniApp(root)

    # keep window open
    root.mainloop()