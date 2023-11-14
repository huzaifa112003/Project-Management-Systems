from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
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
                'SERVER=MAAZ-ULLAH\SQLEXPRESS;'
                'DATABASE=Project;'
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
                'SERVER=MAAZ-ULLAH\SQLEXPRESS;'
                'DATABASE=Project;'
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
        job_title = self.lineEdit_7.text()

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
                INSERT INTO Users (Name, Email, Password, RoleID, JobTitle, DepartmentID)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (name, email, password, role_id, job_title, department_id))
            self.connection.commit()

            QMessageBox.information(self, 'Registration Successful', 'User registered successfully.')
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while registering the user.')

            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

