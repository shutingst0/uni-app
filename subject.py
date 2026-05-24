import random


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
            self.grade = self.grade_from_mark(self.mark)

    def grade_from_mark(self, mark):
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

    def to_dict(self):
        return {
            "id": self.id,
            "mark": self.mark,
            "grade": self.grade
        }
