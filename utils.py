import random

from constants import MAX_SUBJECTS, EMAIL_RE, PASSWORD_RE


def validate_password(password):
    return PASSWORD_RE.match(password) is not None


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
