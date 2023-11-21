class Person:
    # 类变量，用于统计人类的数量，类似java的private生命的私有成员变量
    person_count = 0

    def __init__(self, name):
        self.name = name
        # 每次创建对象时，增加人类数量，相当于两个的构造方法合并了
        Person.person_count += 1
#python默认省略java的无参的构造方法
    @staticmethod
    def initialize_person_count():
        Person.person_count = 0

    @staticmethod
    def get_person_count():
        return Person.person_count


class Employee(Person):
    def __init__(self, name, salary=0):
        super().__init__(name)
        self.salary = salary

    def display_employee_info(self):
        print(f"Employee Name: {self.name}, Salary: {self.salary}")


class Student(Person):
    # 类变量，用于统计学生的数量
    student_count = 0

    def __init__(self, name, student_number=0, grade=0.0):
        super().__init__(name)
        self.student_number = student_number
        self.grade = grade
        # 每次创建学生对象时，增加学生数量
        Student.student_count += 1

    @staticmethod
    def get_student_count():
        return Student.student_count


# 主程序
def main():
    # 1. 创建人类对象并验证
    Person.initialize_person_count()
    person1 = Person("John")
    person2 = Person("Alice")

    print(f"Person Count: {Person.get_person_count()}")  # 输出：Person Count: 2

    # 2. 创建员工类对象并验证
    employee1 = Employee("Bob", 50000)
    employee2 = Employee("Eve", 60000)

    employee1.display_employee_info()
    employee2.display_employee_info()

    # 3. 创建学生类对象并验证
    student1 = Student("Tom", 12345, 90.5)
    student2 = Student("Mary", 67890, 85.5)

    print(f"Student Count: {Student.get_student_count()}")  # 输出：Student Count: 2
    print(f"Person Count: {Person.get_person_count()}")      # 输出：Person Count: 4


if __name__ == "__main__":
    main()
