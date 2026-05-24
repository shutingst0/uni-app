from file import File
from student import Student

DATA_FILE = "students.data"


class StudentDataRepository:
    def __init__(self, filename=DATA_FILE):
        self.students_file = File(filename)

    def _to_student(self, student_dict):
        return Student(student_dict["id"], student_dict["name"], student_dict["email"], student_dict["password"], student_dict.get("subjects", []))

    def _to_dicts(self, students):
        student_dicts = []
        for student in students:
            student_dicts.append(student.to_dict())
        return student_dicts

    def create_student(self, student):
        students = self.read_students()
        students.append(student)
        self.students_file.write(self._to_dicts(students))

    def read_students(self):
        students = []
        for student_dict in self.students_file.read():
            students.append(self._to_student(student_dict))
        return students

    def find_student_by_email(self, email):
        for student in self.read_students():
            if student.email.lower() == email.lower():
                return student

        return None

    def find_student_by_id(self, student_id):
        for student in self.read_students():
            if student.id == student_id:
                return student

        return None

    def update_student(self, updated_student):
        students = self.read_students()

        for i in range(len(students)):
            if students[i].id == updated_student.id:
                students[i] = updated_student
                self.students_file.write(self._to_dicts(students))
                return

        students.append(updated_student)
        self.students_file.write(self._to_dicts(students))

    def remove_student(self, student_id):
        students = self.read_students()
        new_students = []

        for student in students:
            if student.id != student_id:
                new_students.append(student)

        found = len(new_students) != len(students)

        if found:
            self.students_file.write(self._to_dicts(new_students))

        return found

    def clear_students(self):
        self.students_file.write([])
