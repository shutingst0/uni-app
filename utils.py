import random

from constants import MAX_SUBJECTS, EMAIL_RE, PASSWORD_RE


def pad_number(number, length):
    return str(number).zfill(length)


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
