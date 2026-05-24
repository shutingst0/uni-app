import random

from constants import MAX_SUBJECTS, EMAIL_RE, PASSWORD_RE


def validate_password(password):
    return PASSWORD_RE.match(password) is not None


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
