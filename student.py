from utils import grade_from_mark


class Student:
    def __init__(self, student_id, name, email, password, subjects=None):
        self.id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects if subjects is not None else []

    def average_mark(self):
        if len(self.subjects) == 0:
            return 0.0

        total = 0
        for subject in self.subjects:
            total += subject["mark"]

        return total / len(self.subjects)

    def get_result(self):
        mark_average = self.average_mark()
        grade_average = grade_from_mark(mark_average)
        return {"mark_average": mark_average, "grade_average": grade_average}

    def __str__(self):
        result = self.get_result()
        student_info = f"{self.name} :: {self.id} --> Email: {self.email} --> Grade Average: {result['grade_average']} --> Mark Average: {result['mark_average']:.2f}"

        if len(self.subjects) == 0:
            return student_info

        subject_lines = ""
        for subject in self.subjects:
            subject_lines += f"\n  Subject-{subject['id']} --> Mark: {subject['mark']} --> Grade: {subject['grade']}"

        return student_info + subject_lines

    def to_dict(self):
        result = self.get_result()
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": self.subjects,
            "mark_average": result["mark_average"],
            "grade_average": result["grade_average"]
        }
