import random

from utils import grade_from_mark


class Subject:
    def __init__(self, subject_id, mark=None, grade=None):
        self.id = subject_id

        if mark is not None:
            self.mark = mark
        else:
            self.mark = random.randint(25, 100)

        if grade is not None:
            self.grade = grade
        else:
            self.grade = grade_from_mark(self.mark)

    def to_dict(self):
        return {
            "id": self.id,
            "mark": self.mark,
            "grade": self.grade
        }
