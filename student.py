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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": self.subjects
        }
