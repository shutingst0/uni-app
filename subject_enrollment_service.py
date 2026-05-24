import random

from printer import Printer
from subject import Subject

MAX_SUBJECTS = 4
from utils import pad_number


class SubjectEnrollmentService:
    def __init__(self, student_data_repository):
        self.student_data_repository = student_data_repository

    def _generate_subject_id(self, subjects):
        used_ids = []
        for subject in subjects:
            used_ids.append(subject["id"])

        while True:
            new_id = pad_number(random.randint(1, 999), 3)
            if new_id not in used_ids:
                return new_id

    def enrol_subject(self, student_id):
        student = self.student_data_repository.find_student_by_id(student_id)
        if student is None:
            Printer.error("Student does not exist")
            return False

        if len(student.subjects) >= MAX_SUBJECTS:
            Printer.warning("Students are allowed to enrol in 4 subjects only")
            return False

        subject_id = self._generate_subject_id(student.subjects)

        subject = Subject(subject_id).to_dict()
        student.subjects.append(subject)
        self.student_data_repository.update_student(student)

        Printer.success(f"Enrolling in Subject-{subject_id}")
        Printer.info(f"You are now enrolled in {len(student.subjects)} out of 4 subjects")
        return True

    def remove_subject(self, student_id, subject_id):
        student = self.student_data_repository.find_student_by_id(student_id)
        if student is None:
            Printer.error("Student does not exist")
            return False

        new_subjects = []
        found = False

        for subject in student.subjects:
            if subject["id"] == subject_id:
                found = True
            else:
                new_subjects.append(subject)

        if not found:
            Printer.error("Subject does not exist")
            return False

        student.subjects = new_subjects
        self.student_data_repository.update_student(student)

        Printer.success(f"Dropping Subject-{subject_id}")
        return True
