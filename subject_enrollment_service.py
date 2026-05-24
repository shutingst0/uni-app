import random

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
            return None, "Student does not exist"

        if len(student.subjects) >= MAX_SUBJECTS:
            return None, "Students are allowed to enrol in 4 subjects only"

        subject_id = self._generate_subject_id(student.subjects)

        subject = Subject(subject_id).to_dict()
        student.subjects.append(subject)
        self.student_data_repository.update_student(student)

        return subject_id, None

    def remove_subject(self, student_id, subject_id):
        student = self.student_data_repository.find_student_by_id(student_id)
        if student is None:
            return False, "Student does not exist"

        new_subjects = []
        found = False

        for subject in student.subjects:
            if subject["id"] == subject_id:
                found = True
            else:
                new_subjects.append(subject)

        if not found:
            return False, "Subject does not exist"

        student.subjects = new_subjects
        self.student_data_repository.update_student(student)

        return True, None
