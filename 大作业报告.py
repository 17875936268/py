import pymysql

# 员工类
class Employee:
    def __init__(self, ID, name, gender, birth, department, position, phone):
        self.ID = ID
        self.name = name
        self.gender = gender
        self.birth = birth
        self.department = department
        self.position = position
        self.phone = phone

# DatabaseManager 类用于管理数据库操作
class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.employees = []

    # 方法用于建立与数据库的连接
    def connect(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                port=3306,
                user="root",
                password="YES",
                db="员工信息管理系统",  # 数据库名称
                charset="utf8"
            )
            self.cur = self.conn.cursor()
            print("数据库连接成功")  # 连接成功的消息
        except Exception as e:
            print(f"数据库连接失败：{e}")  # 如果连接失败，则显示错误消息

    # 方法用于向数据库添加新员工
    def add_employee_to_db(self, new_employee):
        sql = "INSERT INTO employees (ID, name, gender, birth, department, position, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (int(new_employee.ID), new_employee.name, new_employee.gender, new_employee.birth, new_employee.department, new_employee.position, new_employee.phone)
        try:
            self.cur.execute(sql, values)
            self.conn.commit()  # 提交事务
            self.employees.append(new_employee)  # 将新员工添加到列表中
            print("员工信息添加成功")  # 添加员工成功的消息
        except Exception as e:
            print(f"添加员工失败：{e}")  # 如果添加员工失败，则显示错误消息

    def delete_employee_from_db(self, ID):
        try:
            self.conn.begin()  # 开启事务
            sql = "DELETE FROM employees WHERE ID = %s"
            self.cur.execute(sql, (ID,))
            if self.cur.rowcount > 0:
                self.employees = [e for e in self.employees if e.ID!= ID]  # 从列表中移除已删除的员工
                print("员工信息已删除")  # 删除员工成功的消息
            else:
                print("未找到该员工信息")  # 如果找不到员工信息，则显示消息
            self.conn.commit()  # 提交事务
        except Exception as e:
            self.conn.rollback()  # 回滚事务
            print(f"删除员工失败，错误原因: {e}")  # 如果删除员工失败，则显示错误消息

    # 方法用于修改数据库中的员工信息
    def update_employee_in_db(self, ID, updated_employee):
        try:
            sql = "SELECT * FROM employees WHERE ID = %s"
            self.cur.execute(sql, (ID,))
            if self.cur.rowcount == 0:
                print("ID 不存在")
                return
            sql = "UPDATE employees SET name = %s, gender = %s, birth = %s, department = %s, position = %s, phone = %s WHERE ID = %s"
            values = (updated_employee.name, updated_employee.gender, updated_employee.birth, updated_employee.department, updated_employee.position, updated_employee.phone, ID)
            self.cur.execute(sql, values)
            for e in self.employees:  # 在列表中更新员工信息
                if e.ID == int(ID):
                    e.name = updated_employee.name
                    e.gender = updated_employee.gender
                    e.birth = updated_employee.birth
                    e.department = updated_employee.department
                    e.position = updated_employee.position
                    e.phone = updated_employee.phone
            self.conn.commit()  # 提交事务
            print("员工信息已更新")  # 更新员工成功的消息
        except Exception as e:
            print(f"更新员工失败：{e}")  # 如果更新员工失败，则显示错误消息

    # 方法用于搜索员工信息
    def search_employee_from_db(self, search_attribute, search_value):
        sql = f"SELECT * FROM employees WHERE {search_attribute} = %s"
        try:
            self.cur.execute(sql, (search_value,))
            rows = self.cur.fetchall()
            employees = []
            for row in rows:
                employee_dict = {
                    "ID": row[0],
                    "name": row[1],
                    "gender": row[2],
                    "birth": row[3],
                    "department": row[4],
                    "position": row[5],
                    "phone": row[6]
                }
                employees.append(employee_dict)
            return employees
        except Exception as e:
            print(f"搜索员工失败：{e}")  # 如果搜索员工失败，则显示错误消息
            return None

# 用户界面类
class UserInterface:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # 菜单方法
    def menu(self):
        while True:
            print("\n员工信息管理系统")
            print("1. 添加员工信息")
            print("2. 删除员工信息")
            print("3. 更新员工信息")
            print("4. 查询员工信息")
            print("5. 退出系统")
            choice = input("请选择操作：")

            if choice == '1':
                ID = input("请输入员工编号：")
                name = input("请输入员工姓名：")
                gender = input("请输入性别：")
                birth = input("请输入出生日期：")
                department = input("请输入部门：")
                position = input("请输入职位：")
                phone = input("请输入电话：")
                new_employee = Employee(int(ID), name, gender, birth, department, position, phone)
                self.db_manager.add_employee_to_db(new_employee)
            elif choice == '2':
                ID = input("请输入要删除的员工编号：")
                self.db_manager.delete_employee_from_db(ID)
                # 用户界面类中的更新员工信息部分
            elif choice == '3':
                ID = input("请输入要更新的员工编号：")
                # 检查数据库中是否存在要更新的员工ID
                employee_exists = False
                for employee in self.db_manager.employees:
                    if employee.ID == int(ID):
                        employee_exists = True
                        break
                if not employee_exists:
                    print("错误：未找到此员工 ID，请输入正确的员工 ID。")
                else:
                    name = input("请输入修改后的员工姓名：")
                    gender = input("请输入修改后的性别：")
                    birth = input("请输入修改后的出生日期：")
                    department = input("请输入修改后的部门：")
                    position = input("请输入修改后的职位：")
                    phone = input("请输入修改后的电话：")
                    updated_employee = Employee(ID, name, gender, birth, department, position, phone)
                    self.db_manager.update_employee_in_db(ID, updated_employee)
            elif choice == '4':
                search_attribute = input("请输入要查询的属性（ID/name/gender/birth/department/position/phone）：")
                search_value = input("请输入要查询的值：")
                employees = self.db_manager.search_employee_from_db(search_attribute, search_value)
                if employees:
                    for employee in employees:
                        print(
                            f"员工编号:{employee['ID']}，姓名：{employee['name']}，性别：{employee['gender']}，出生日期：{employee['birth']}，部门：{employee['department']}，职位：{employee['position']}，电话：{employee['phone']}")
                else:
                    print("未找到符合条件的员工信息")
            elif choice == '5':
                break
            else:
                print("请选择正确的操作")
# 创建数据库管理对象并连接
db_manager = DatabaseManager()
db_manager.connect()

# 创建用户界面对象并运行菜单
ui = UserInterface(db_manager)
ui.menu()