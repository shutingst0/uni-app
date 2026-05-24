from subject_enrollment_service import MAX_SUBJECTS


class AdminService:
    def __init__(self, student_data_repository):
        self.student_data_repository = student_data_repository

    def get_all_students(self):
        return self.student_data_repository.read_students()

    def group_students(self):
        students = self.student_data_repository.read_students()

        groups = {
            "HD": [],
            "D": [],
            "C": [],
            "P": [],
            "Z": []
        }

        for student in students:
            result = student.get_result()
            groups[result["grade_average"]].append(student)

        return groups

    def partition_students(self):
        students = self.student_data_repository.read_students()

        pass_students = []
        fail_students = []

        for student in students:
            result = student.get_result()
            has_full_subjects = len(student.subjects) == MAX_SUBJECTS
            is_passing = has_full_subjects and result["mark_average"] >= 50

            if is_passing:
                pass_students.append(student)
            else:
                fail_students.append(student)

        return pass_students, fail_students

    def remove_student(self, student_id):
        is_removed = self.student_data_repository.remove_student(student_id)

        if is_removed:
            print("Removing Student", student_id, "Account")
        else:
            print("Student", student_id, "does not exist")

        return is_removed

    def clear_students(self):
        self.student_data_repository.clear_students()
        print("Students data cleared")
