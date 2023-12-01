from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem
from PyQt6.uic import loadUi
import sys
import pyodbc

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        loadUi('mainlogin.ui', self)

        # Connect to the SQL Server database
        try:
            self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-NBH907Q\KNIGHT;'    
                'DATABASE=proj;'
                'Trusted_Connection=yes;'
            )

            # Create a cursor
            self.cursor = self.connection.cursor()

            print("Connected to the database.")
        except pyodbc.Error as e:
            print(f"Database connection error: {e}")
            # Handle the exception (e.g., display an error message)


        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)

    
    def login(self):
        # Get the entered email and password
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # Query the database to check credentials
        query = "SELECT COUNT(*) FROM Users WHERE Email = ? AND Password = ?"
        result = self.cursor.execute(query, (email, password)).fetchone()

        # Check if the credentials are correct
        if result and result[0] > 0:
            QMessageBox.information(self, 'Login Successful', 'Login Successful')

            # Retrieve the UserID for the logged-in user
            user_query = "SELECT UserID FROM Users WHERE Email = ?"
            user_id_result = self.cursor.execute(user_query, (email,)).fetchone()

            if user_id_result:
                user_id = user_id_result[0]
                # Open the project screen and pass the user_id
                self.project_screen = ProjectScreen(user_id)
                self.project_screen.show()

                # Close the main window
                self.close()
            else:
                QMessageBox.warning(self, 'User ID not found', 'Failed to retrieve User ID.')
        else:
            QMessageBox.warning(self, 'Incorrect Email or Password', 'Incorrect Email or Password')

    def register(self):
        # Open the registration form
        self.register = RegisterForm()
        self.register.show()


class RegisterForm(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('register.ui', self)

        # Establish the database connection
        self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-NBH907Q\KNIGHT;'
                'DATABASE=proj;'
                'Trusted_Connection=yes;'
        )
        self.cursor = self.connection.cursor()

        self.lineEdit_3.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_4.setEchoMode(QLineEdit.EchoMode.Password)
        self.pushButton.clicked.connect(self.register)
        self.load_roles()
        self.load_departments()

    def load_roles(self):
        try:
            # Retrieve roles from the database
            role_query = "SELECT RoleName FROM Role"
            roles = self.cursor.execute(role_query).fetchall()

            # Load roles into the combobox
            self.comboBox_2.addItems([role[0] for role in roles])
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while loading roles.')

    def load_departments(self):
        try:
            # Retrieve departments from the database
            department_query = "SELECT DepartmentName FROM Department"
            departments = self.cursor.execute(department_query).fetchall()

            # Load departments into the combobox
            self.comboBox.addItems([department[0] for department in departments])
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while loading departments.')

    def register(self):
        # Get the entered values from the registration form
        name = self.lineEdit.text()
        email = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        confirm_password = self.lineEdit_4.text()

        # Get selected role and department from the comboboxes
        role_name = self.comboBox_2.currentText()
        department_name = self.comboBox.currentText()

        # Check if the password and confirm password match
        if password != confirm_password:
            QMessageBox.warning(self, 'Password Mismatch', 'Password and Confirm Password do not match.')
            return

        try:
            # Check if the email already exists in the Users table
            email_check_query = "SELECT COUNT(*) FROM Users WHERE Email = ?"
            email_count = self.cursor.execute(email_check_query, (email,)).fetchone()[0]

            if email_count > 0:
                QMessageBox.warning(self, 'Email Already Exists', 'Email address is already registered.')
                return

            # Retrieve RoleID for the given RoleName
            role_query = "SELECT RoleID FROM Role WHERE RoleName = ?"
            role_result = self.cursor.execute(role_query, (role_name,)).fetchone()

            if not role_result:
                QMessageBox.warning(self, 'Role not found', f'Role "{role_name}" not found.')
                return

            role_id = role_result[0]

            # Retrieve DepartmentID for the given DepartmentName
            department_query = "SELECT DepartmentID FROM Department WHERE DepartmentName = ?"
            department_result = self.cursor.execute(department_query, (department_name,)).fetchone()

            if not department_result:
                QMessageBox.warning(self, 'Department not found', f'Department "{department_name}" not found.')
                return
            

            department_id = department_result[0]
            

            # Insert a new user into the Users table
            insert_query = """
                INSERT INTO Users (Name, Email, Password, RoleID, DepartmentID)
                VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (name, email, password, role_id, department_id))
            self.connection.commit()

            QMessageBox.information(self, 'Registration Successful', 'User registered successfully.')
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while registering the user.')


# class Project(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         loadUi('project.ui', self)
#         #self.resize(1024, 768)

#         # Establish the database connection
#         self.connection = pyodbc.connect(
#                 'DRIVER={ODBC Driver 17 for SQL Server};'
#                 'SERVER=DESKTOP-NBH907Q\KNIGHT;'
#                 'DATABASE=proj;'
#                 'Trusted_Connection=yes;'
#         )
#         self.cursor = self.connection.cursor()

#         self.pushButton.clicked.connect(self.create_project)
#         # self.pushButton_3.clicked.connect(self.edit_task)
#         self.load_data_into_table()

        
#     def load_data_into_table(self):
#         # Clear the table first
#         self.tableWidget.setRowCount(0)

#         # Define your query to fetch data
#         query = "SELECT ProjectName, Description, StartDate, EndDate FROM Project"
#         try:
#             self.cursor.execute(query)
#             for row_number, row_data in enumerate(self.cursor):
#                 # print(f"Row {row_number}: {row_data}")  # Debugging line
#                 self.tableWidget.insertRow(row_number)
#                 for column_number, data in enumerate(row_data):
#                     # print(f"Column {column_number}: {data}")  # Debugging line
#                     self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
#         except pyodbc.Error as e:
#             print(f"Error loading data into table: {e}")
#             QMessageBox.warning(self, 'Database Error', 'An error occurred while loading data into the table.')

#         self.tableWidget.update()  # Refresh the UI

#     def create_project(self):
#         self.create_project = CreateProject()
#         self.create_project.show()
    
#     # def edit_task(self):
#     #     self.edit_task = CreateTask()
#     #     self.edit_task.show()

class ProjectScreen(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        loadUi('project.ui', self)

        # Establish the database connection
        self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-NBH907Q\KNIGHT;'
                'DATABASE=proj;'
                'Trusted_Connection=yes;'
        )
        self.cursor = self.connection.cursor()
        self.pushButton.clicked.connect(self.create_project)
        # Save the user ID for later use
        self.user_id = user_id

        # Populate the table with projects for the logged-in user
        self.populate_project_table()

    def populate_project_table(self):
        try:
            # Query to retrieve projects for the logged-in user as manager
            manager_query = """
                SELECT ProjectName, Description, StartDate, EndDate
                FROM Project
                WHERE ManagerID = ?
            """

            # Query to retrieve projects for the logged-in user as worker/member
            worker_query = """
                SELECT ProjectName, Description, StartDate, EndDate
                FROM Project
                WHERE ProjectID IN (
                    SELECT ProjectID
                    FROM Task
                    WHERE AssigneeID = ?
                )
            """

            # Retrieve the logged-in user's ID
            user_id = self.user_id

            # Check if the logged-in user is a manager
            manager_result = self.cursor.execute(manager_query, (user_id,)).fetchall()

            # If not a manager, retrieve projects as a worker/member
            if not manager_result:
                projects = self.cursor.execute(worker_query, (user_id,)).fetchall()
            else:
                projects = manager_result

            # Set the number of rows in the table
            self.tableWidget.setRowCount(len(projects))

            # Populate the table with project details
            for row, project in enumerate(projects):
                for col, value in enumerate(project):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row, col, item)

            # Set the column headers
            headers = ["Project Name", "Description", "Start Date", "End Date"]
            self.tableWidget.setHorizontalHeaderLabels(headers)

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while retrieving project details.')

        self.tableWidget.update()  # Refresh the UI

    def create_project(self):
        self.create_project = CreateProject()
        self.create_project.show()
    


class CreateProject(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('createditproject.ui', self)

        # Establish the database connection
        self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-NBH907Q\KNIGHT;'
                'DATABASE=proj;'
                'Trusted_Connection=yes;'
        )
        self.cursor = self.connection.cursor()
        self.pushButton.clicked.connect(self.create_project)

    def create_project(self):
        # Get the entered project information from the UI
        project_name = self.lineEdit.text()
        description = self.lineEdit_5.text()
        start_date = self.dateEdit_2.date().toString("yyyy-MM-dd")
        end_date = self.dateEdit_3.date().toString("yyyy-MM-dd")
        client_name = self.comboBox.currentText()  # Assuming this is the client's name

        # First, retrieve the ClientID from the Client table
        client_id_query = "SELECT ClientID FROM Client WHERE ClientName = ?"
        try:
            self.cursor.execute(client_id_query, (client_name))
            client_id_result = self.cursor.fetchone()
            print(client_id_result)
            if client_id_result:
                client_id = client_id_result[0]

                # Insert the project information into the database
                print("Error")
                project_query = """
                    INSERT INTO Project (ProjectName, Description, StartDate, EndDate, ClientID) 
                    VALUES (?, ?, ?, ?, ?)
                """
                self.cursor.execute(project_query, (project_name, description, start_date, end_date, client_id))
                self.connection.commit()
                QMessageBox.information(self, 'Success', 'Project saved successfully.')
            else:
                QMessageBox.warning(self, 'Error', 'Client not found.')
        except pyodbc.Error as e:
            print(f"Error in database operation: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred during the database operation.')

        self.close()



class Task(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('task.ui', self)
        #self.resize(1024, 768)

        # Establish the database connection
        self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-NBH907Q\KNIGHT;'
                'DATABASE=proj;'
                'Trusted_Connection=yes;'
        )
        self.cursor = self.connection.cursor()

        self.pushButton.clicked.connect(self.create_task)
        self.pushButton_3.clicked.connect(self.edit_task)
        self.load_data_into_table()

    def load_data_into_table(self):
        # Clear the table first
        self.tableWidget.setRowCount(0)

        # Define your query to fetch data
        query = "SELECT TaskName, Description, StartDate, EndDate, StatusName as Status FROM Task T join TaskStatus TS on T.StatusID = TS.StatusID"
        try:
            self.cursor.execute(query)
            for row_number, row_data in enumerate(self.cursor):
                # print(f"Row {row_number}: {row_data}")  # Debugging line
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    # print(f"Column {column_number}: {data}")  # Debugging line
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except pyodbc.Error as e:
            print(f"Error loading data into table: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while loading data into the table.')

        self.tableWidget.update()  # Refresh the UI

    def create_task(self):
        self.create_task = CreateTask()
        self.create_task.show()
    
    def edit_task(self):
        self.edit_task = CreateTask()
        self.edit_task.show()

            


class CreateTask(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('createditasks.ui', self)

        # Establish the database connection
        self.connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-NBH907Q\KNIGHT;'
                'DATABASE=proj;'
                'Trusted_Connection=yes;'
        )
        self.cursor = self.connection.cursor()

    def save_task(self):
        # Get the entered task information from the UI
        task_name = self.taskNameLineEdit.text()
        description = self.descriptionTextEdit.toPlainText()
        start_date = self.startDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.endDateEdit.date().toString("yyyy-MM-dd")
        status = self.statusComboBox.currentText()

        # Insert the task information into the database
        query = "INSERT INTO Task (TaskName, Description, StartDate, EndDate, StatusID) VALUES (?, ?, ?, ?, ?)"
        try:
            self.cursor.execute(query, task_name, description, start_date, end_date, status)
            self.connection.commit()
            QMessageBox.information(self, 'Success', 'Task saved successfully.')
        except pyodbc.Error as e:
            print(f"Error saving task: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while saving the task.')

        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())