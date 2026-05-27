# region Yuhang Wang
import json
import os
import random
import re


DATA_FILE = "students.data" 
# File that reserves students' information
MAX_SUBJECTS = 4

EMAIL_REGEX = r"^[A-Za-z]+\.[A-Za-z]+@university\.com$" 
# Email format
PASSWORD_REGEX = r"^[A-Z][A-Za-z]{4,}\d{3,}$" 
# Password format


# =========================
# Model Classes
# =========================

class Subject:
    def __init__(self, subject_id, mark, grade):
        self.id = subject_id
        self.mark = mark
        self.grade = grade

    def to_dict(self): # Change list into dictionary
        return {
            "id": self.id,
            "mark": self.mark,
            "grade": self.grade
        }

class Student:
    def __init__(self, student_id, name, email, password, subjects=None):
        self.id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects if subjects is not None else []

    def average_mark(self):
        if len(self.subjects) == 0: 
        # If the student have not chosen a subject, his avg_mark would be 0
            return 0.0

        total = 0
        for subject in self.subjects:
            total += subject["mark"]

        return total / len(self.subjects)

    def to_dict(self): # Change list into dictionary
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": self.subjects
        }


# =========================
# Database Class
# =========================

class Database:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.create_file_if_missing()

    def create_file_if_missing(self): 
    # This function is for creating file if it doesn't exist
        if not os.path.exists(self.filename): 
        # Not + (not exist = False) = True
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file) 
                # Use none to fill the file

    def read_students(self):
        self.create_file_if_missing()

        try:
            with open(self.filename, "r", encoding="utf-8") as file: 
            # Read model
                data = json.load(file) 
                # Read from file

            if isinstance(data, list): 
            # Make sure we return a list
                return data

            return []

        except json.JSONDecodeError:
            print("Database file is damaged. Starting with empty data.")
            return []

    def write_students(self, students):
        with open(self.filename, "w", encoding="utf-8") as file: 
        # Write model
            json.dump(students, file, indent=2) 
            # Write into file

    def clear_students(self):
        self.write_students([]) 
        # To clear data, use none to cover previous file

    def find_student_by_email(self, email):
        students = self.read_students()

        for student in students:
            if student["email"].lower() == email.lower(): 
            # If the email of student == email chosen
                return student

        return None

    def find_student_by_id(self, student_id):
        students = self.read_students()

        for student in students:
            if student["id"] == student_id: # If the id of student == id chosen
                return student

        return None

    def save_student(self, updated_student):
        students = self.read_students()

        for i in range(len(students)):
            if students[i]["id"] == updated_student["id"]: 
            # Change the NO.i attribute in student into a new one
                students[i] = updated_student
                self.write_students(students)
                return

        students.append(updated_student) 
        # Add the 'updated_student' into 'students'
        self.write_students(students) 
        # Save new data

    def remove_student(self, student_id):
        students = self.read_students()
        new_students = []

        found = False

        for student in students:
            if student["id"] == student_id:
                found = True 
                # If we can find the student we want to remove, then change 'found' from False into True but don't write the information of this student into file 2
            else:
                new_students.append(student) 
                # If the student is not that one we want to remove, add his(her) information into file 2

        if found: 
        # If 'Found' is still False, it means all students selected should not be removed, then we have no need to change the file
            self.write_students(new_students) 
            # If 'Found' is True, it means at least one student is removed, use new file 2 to cover previous one

        return found


db = Database()

# region Shuting Yang
# =========================
# Account Service
# =========================

class AccountService:
    def __init__(self, students=None):
        self.students = [self._from_dict(s) for s in students] if students else []

    def _from_dict(self, student_dict):
        return Student(student_dict["id"], student_dict["name"], student_dict["email"], student_dict["password"], student_dict.get("subjects", []))

    def validate(self, email, password):
        valid_email = bool(re.match(EMAIL_REGEX, email))
        valid_password = bool(re.match(PASSWORD_REGEX, password))

        print(f"email {valid_email}")
        print(f"password {valid_password}")

        if valid_password is False or valid_email is False:
            print("Incorrect email or password format")
            return False

        print("Email and password format acceptable")
        return True

    def check_duplicate(self, new_student):
        for existing_student in self.students:
            if new_student.email.lower() == existing_student.email.lower():
                print(f"Student with email {new_student.email} already exists")
                return True

        return False

    def generate_unique_student_id(self):
        existing_ids = {s.id for s in self.students}

        while True:
            new_id = f"{random.randint(1, 999999):06d}"

            if new_id not in existing_ids:
                return new_id

    def register(self, name, email, password):
     
        name = name.strip()
        email = email.strip().lower()
        password = password.strip()

        if name == "":
            print("Name cannot be empty")
            return None

        is_valid = self.validate(email, password)

        if is_valid is not True:
            return None

        student_id = self.generate_unique_student_id()
        student = Student(student_id, name, email, password)

        has_duplicate = self.check_duplicate(student)

        if has_duplicate is True:
            return None

        self.students.append(student)

        print(f"Signed up student {student.name}")
        print("Student ID:", student.id)

        return student.to_dict()

    def login(self, email, password):
        email = email.strip().lower()
        password = password.strip()

        is_valid = self.validate(email, password)

        if is_valid is not True:
            return None

        for existing_student in self.students:
            if (
                email == existing_student.email.lower()
                and password == existing_student.password
            ):
                print("Login successful")
                return existing_student.to_dict()

        print("Student does not exist")
        return None


# =========================
# Helper Functions
# =========================

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


def generate_subject_id(subjects):
    used_ids = []

    for subject in subjects:
        used_ids.append(subject["id"])

    while True:
        new_id = str(random.randint(1, 999)).zfill(3)

        if new_id not in used_ids:
            return new_id


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

    students = db.read_students()
    account_service = AccountService(students)

    new_student = account_service.register(name, email, password)

    if new_student is None:
        return

    db.save_student(new_student)


def login_student():
    print("Student Sign In")

    email = input_text("Email: ")
    password = input_text("Password: ")

    students = db.read_students()
    account_service = AccountService(students)

    student = account_service.login(email, password)

    if student is None:
        return

    subject_menu(student["id"])

# region Ming Sun
# =========================
# Subject Enrolment System
# =========================
#subject_menu(student_id) is the course menu after student login.
#The program uses while True to create a loop menu until the student enters x to exit.
#User input uses .strip().lower() to remove spaces and convert to lowercase.
#c change password,e enrol subject,r remove subject,s show subjects,x exit system

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
#find student use student_id
    student = db.find_student_by_id(student_id)
#  if student is None return error
    if student is None:
        print("Student does not exist")
        return
# user set password and confirm
    new_password = input_text("New Password: ").strip()
    confirm_password = input_text("Confirm Password: ").strip()
# Determine if password consistent
    if new_password != confirm_password:
        print("Password does not match - try again")
        return
# if password consistent, follow the rule whether ture
    valid_password = bool(re.fullmatch(PASSWORD_REGEX, new_password))

    if valid_password is False:
        print("Incorrect password format")
        return
# reset password successful
    student["password"] = new_password
    db.save_student(student)

    print("Password updated successfully")


def enrol_subject(student_id):
    #find student use student_id
    student = db.find_student_by_id(student_id)
#  if student is None return error
    if student is None:
        print("Student does not exist")
        return

    subjects = student["subjects"]
#Students can register for a maximum of 4 courses.If they exceed this limit, return false
    if len(subjects) >= MAX_SUBJECTS:
        print("Students are allowed to enrol in 4 subjects only")
        return
# create a new subject ID and makes sure it is unique.
    subject_id = generate_subject_id(subjects)
# random mark 25-100
    mark = random.randint(25, 100)
#grade(P、C、D、HD) relate to mark
    grade = grade_from_mark(mark)
#Creates a subject object and converts it into dictionary format for saving.
    subject = Subject(subject_id, mark, grade).to_dict()
#Adds the new subject into the student’s subject list.
    subjects.append(subject)

    db.save_student(student)

    print("Enrolling in Subject-" + subject_id)
    print("You are now enrolled in", len(subjects), "out of 4 subjects")


def remove_subject(student_id):
    student = db.find_student_by_id(student_id)

    if student is None:
        print("Student does not exist")
        return
# find subject_id
    subject_id = input_text("Remove Subject by ID: ").strip()
# .isdigit() checks whether the input contains only numbers.
#If it is numeric, .zfill(3) automatically adds leading zeros to make it 3 digits.
    if subject_id.isdigit():
        subject_id = subject_id.zfill(3)
# check subject_id whether 3 digit
    if len(subject_id) != 3 or not subject_id.isdigit():
        print("Invalid subject ID")
        return

    subjects = student["subjects"]
    new_subjects = []

    found = False
#If the subject ID matches, the subject to remove is found.
    for subject in subjects:
        if subject["id"] == subject_id:
            found = True
        else:
            new_subjects.append(subject)
#Checks whether the subject actually exists.
    if not found:
        print("Subject does not exist")
        return
#Replaces the old subject list with the new list.
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
# if student dont choose subject,return Nothing to Display
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
#c clear database,g group students by grade,p partition pass/fail students,r remove student,s show all students,x exit system
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
# if dont have students,print Nothing to Display
    if len(students) == 0:
        print("< Nothing to Display >")
        return
# show details
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
# use for student in students to loop through all students.
    for student in students:
        # Calculates the student grade based on average mark.
        grade = student_grade(student)
        # Adds the student into the corresponding grade group.
        groups[grade].append(student)

    for grade in groups:
        if len(groups[grade]) > 0:
            print(grade, "-->", end=" ")

            for student in groups[grade]:
                #Calculates the student average mark.
                avg = average_mark(student)
                print(
                    "[" + student["name"],
                    "::",
                    student["id"],
                    "--> GRADE:",
                    grade,
                    "--> MARK:",
                    # Formats the average mark to 2 decimal places.
                    format(avg, ".2f") + "]",
                    end=" "
                )

            print()

# this funcation：students are categorized into F and P based on their mark.
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

#This funcation is used to format the student list into a readable string showing student name, ID, grade, and average mark.
#The program displays student name, ID, grade, and average mark.
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
    # Determine if the student ID is valid
    student_id = input_text("Remove by ID: ").strip()

    if len(student_id) != 6 or not student_id.isdigit():
        print("Invalid student ID")
        return

    removed = db.remove_student(student_id)
#If it is reasonable to determine whether the student ID exists...
    if removed:
        print("Removing Student", student_id, "Account")
    else:
        print("Student", student_id, "does not exist")

#The program first asks the admin for confirmation and uses .strip().lower() to process the input.
#If the input is y or yes, the system calls db.clear_students() to clear the database.Otherwise, the system cancels the operation and shows Clear cancelled.
def clear_database():
    print("Clearing students database")

    answer = input_text("Are you sure you want to clear the database (Y)ES/(N)O: ")
    answer = answer.strip().lower()

    if answer == "y" or answer == "yes":
        db.clear_students()
        print("Students data cleared")
    else:
        print("Clear cancelled")

# region Jinjie Deng
# =========================
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
