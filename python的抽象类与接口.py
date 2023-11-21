# 1. 定义接口，省略abstract关键字
class Eligible:
    def is_eligible(self):
        pass

# 2. 抽象员工类，直接从装饰器模块导入需要继承和实现的抽象类方法
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def calculate_salary(self):
        pass

# 3. 教师类，继承员工类并实现接口
class Teacher(Employee, Eligible):
    def __init__(self, name, research_points, basic_salary, position_salary):
        super().__init__(name)
        self.research_points = research_points
        self.basic_salary = basic_salary
        self.position_salary = position_salary
#代替toString方法
    def __str__(self):
        return f"Teacher(name={self.name}, research_points={self.research_points}, " \
               f"basic_salary={self.basic_salary}, position_salary={self.position_salary})"

    def calculate_salary(self):
        return self.basic_salary + self.position_salary

    def is_eligible(self):
        return self.research_points > 100

# 4. 销售员类，继承员工类
class Salesperson(Employee, Eligible):
    def __init__(self, name, sales_quantity, unit_price):
        super().__init__(name)
        self.sales_quantity = sales_quantity
        self.unit_price = unit_price

    def __str__(self):
        return f"Salesperson(name={self.name}, sales_quantity={self.sales_quantity}, " \
               f"unit_price={self.unit_price})"

    def calculate_salary(self):
        return self.sales_quantity * self.unit_price

    def is_eligible(self):
        return self.sales_quantity * self.unit_price > 5000

# 测试
if __name__ == "__main__":
    # 创建教师对象并验证
    teacher = Teacher("John Doe", 120, 50000, 10000)
    print(teacher)
    print("Total Salary:", teacher.calculate_salary())
    print("Eligible:", teacher.is_eligible())

    # 创建销售员对象并验证
    salesperson = Salesperson("Jane Doe", 100, 60)
    print(salesperson)
    print("Total Salary:", salesperson.calculate_salary())
    print("Eligible:", salesperson.is_eligible())
