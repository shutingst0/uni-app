from student import Student #"从 student.py 文件里，把 Student 类拿过来用"  
import re

class AccountServicd:
    def __init__(self):
        self.students = [] #要把注册完的学生存在这里
        
    def validate(self, email, password):     #只负责检查，返回ture or false
        valid_email = bool(re.match(r"[^@]+@university\.com$", email)) # bool 会判断值是否为True or False, re.match只会返还string
        valid_password = bool(re.match(r"[A-Z][a-zA-Z]{4,}\d{3,}", password))
        
        if valid_password is False or valid_email is False:
            print("Incorrect email or password format")
            return False
        
        print("email and password format acceptable")
        return True
    
    def check_duplicate(self, new_student):
        for existing_student in self.students: #前面的existing_student是我自己取的名字
            if new_student.email == existing_student.email:
                print(f"Student with email {new_student.email} already exist")
                return True
        
        return False
    
    def register(self, name, email, password):    #负责整个流程
        is_valid = self.validate(email, password) # 先检查邮箱和密码格式是否正确，通过才继续。
        if is_valid is not True:
            return

        student = Student(name,email,password)     #创建一个新的学生对象

        has_duplicate = self.check_duplicate(student)
        if has_duplicate is True:
            return
                
        self.students.append(student)       #把这个新学生加入列表
        print(f"Signed up student {student.name}")
        return student
    
    def login(self, email, password):
        is_valid = self.validate(email, password)
        if is_valid is not True:
            return 
        for existing_student in self.students:
            if email == existing_student.email and password == existing_student.password:
                print(f"Login successdul")
                return existing_student
            
        print("Student does not exist")
        return None
