class Subject:
    def __init__(self, subject_id, mark, grade):
        self.id = subject_id
        self.mark = mark
        self.grade = grade

    def to_dict(self):
        return {
            "id": self.id,
            "mark": self.mark,
            "grade": self.grade
        }
