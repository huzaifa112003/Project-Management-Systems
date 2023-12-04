from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QTableWidgetItem
from PyQt6.QtCore import QDate, pyqtSignal
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
        self.pushButton_2.clicked.connect(self.delete_project)
        self.pushButton_3.clicked.connect(self.edit_project)
        self.pushButton_4.clicked.connect(self.open_project)
        # Save the user ID for later use
        self.user_id = user_id

        # Populate the table with projects for the logged-in user
        self.populate_project_table()

    def is_manager(self, user_id):
        # Check if the user is the manager based on the user ID
        return user_id == 1

    def populate_project_table(self):
        try:
            # Determine if the logged-in user is a manager
            user_is_manager = self.is_manager(self.user_id)

            # Query to retrieve projects for the logged-in user as manager
            manager_query = """
                SELECT ProjectID, ProjectName, Description, StartDate, EndDate, ClientName
                FROM Project
                INNER JOIN Client ON Project.ClientID = Client.ClientID
                WHERE ManagerID = ?
            """

            # Query to retrieve projects for the logged-in user as worker/member
            worker_query = """
                SELECT ProjectID, ProjectName, Description, StartDate, EndDate, ClientName
                FROM Project
                INNER JOIN Client ON Project.ClientID = Client.ClientID
                WHERE ProjectID IN (
                    SELECT ProjectID
                    FROM Task
                    WHERE AssigneeID = ?
                )
            """

            # Retrieve projects based on the user's role
            if user_is_manager:
                projects = self.cursor.execute(manager_query, (self.user_id,)).fetchall()
            else:
                projects = self.cursor.execute(worker_query, (self.user_id,)).fetchall()

            # Set the number of rows in the table
            self.tableWidget.setRowCount(len(projects))

            # Populate the table with project details
            for row, project in enumerate(projects):
                for col, value in enumerate(project):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row, col, item)

            # Set the column headers
            headers = ["Project ID", "Project Name", "Description", "Start Date", "End Date", "Client Name"]
            self.tableWidget.setHorizontalHeaderLabels(headers)
            self.tableWidget.hideColumn(0)

            # Enable/disable buttons based on the user's role
            self.pushButton.setVisible(user_is_manager)
            self.pushButton_3.setVisible(user_is_manager)
            self.pushButton_2.setVisible(user_is_manager)

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while retrieving project details.')

        self.tableWidget.update()  # Refresh the UI

    def create_project(self):
        self.create_project = CreateProject()
        self.create_project.show()

    def edit_project(self):
        # Get the selected project details
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'No Project Selected', 'Please select a project to edit.')
            return

        # Retrieve the ProjectID
        project_id = int(self.tableWidget.item(selected_row, 0).text())

        # Retrieve other project details
        project_details = [self.tableWidget.item(selected_row, col).text() for col in
                        range(1, self.tableWidget.columnCount())]

        # Pass the project details and ProjectID to the EditProject screen
        self.edit_project = EditProject(project_id, project_details)
        self.edit_project.editing_complete.connect(self.populate_project_table)
        self.edit_project.show()

    def delete_project(self):
        # Get the selected project details
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, 'No Project Selected', 'Please select a project to delete.')
            return

        # Confirm deletion
        confirm_msg = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete this project?\nThis will delete all related tasks and reports.',
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if confirm_msg == QMessageBox.StandardButton.Yes:
            # Retrieve the ProjectID
            project_id = int(self.tableWidget.item(selected_row, 0).text())

            # Delete related tasks and reports
            self.delete_related_tasks_and_reports(project_id)

            # Delete the project
            self.delete_project_record(project_id)

            # Refresh the project table
            self.populate_project_table()

    def delete_related_tasks_and_reports(self, project_id):
        try:
            # Delete related tasks
            task_delete_query = "DELETE FROM Task WHERE ProjectID = ?"
            self.cursor.execute(task_delete_query, (project_id,))
            self.connection.commit()

            # Delete related reports
            report_delete_query = "DELETE FROM Report WHERE ProjectID = ?"
            self.cursor.execute(report_delete_query, (project_id,))
            self.connection.commit()

        except pyodbc.Error as e:
            print(f"Error deleting related tasks and reports: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while deleting related tasks and reports.')

    def delete_project_record(self, project_id):
        try:
            # Delete the project
            project_delete_query = "DELETE FROM Project WHERE ProjectID = ?"
            self.cursor.execute(project_delete_query, (project_id,))
            self.connection.commit()

            QMessageBox.information(self, 'Success', 'Project deleted successfully.')

        except pyodbc.Error as e:
            print(f"Error deleting project: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while deleting the project.')

    def get_selected_project_data(self):
        current_row = self.tableWidget.currentRow()  # Get the currently selected row index
        if current_row != -1:  # Check if a row is actually selected
            project_id_item = self.tableWidget.item(current_row, 0)  # 0 is assuming ProjectID is in the first column
            project_name_item = self.tableWidget.item(current_row, 1)  # Project name in the second column
            if project_id_item and project_name_item:
                project_id = project_id_item.text()
                project_name = project_name_item.text()
                return project_id, project_name
        return None, None # Return None or handle the case when no row is selected
        
    # def open_project(self):
    #     self.open_project = Task()
    #     self.open_project.show()
    def open_project(self):
        # project_id = self.get_selected_project_id()
        project_id, project_name = self.get_selected_project_data()
        if project_id and project_name:
            self.open_projectasks_window = Task(project_id, project_name)
            self.open_projectasks_window.show()
            # self.open_project_window.load_tasks()  # Call the method to load the tasks for this project ID
            # self.open_project_window.show()  # Show the Task window
        else:
            # Handle the case when no project is selected (e.g., show an error message)
            print("Please select a project first.")



class EditProject(QMainWindow):

    editing_complete = pyqtSignal()

    def __init__(self, project_id, project_details):
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

        self.project_id = project_id
        self.project_details = project_details

        # Populate the fields with the existing project details
        self.lineEdit.setText(project_details[0])  # Project Name
        self.lineEdit_5.setText(project_details[1])  # Description
        # Set the start and end dates using QDate
        start_date = QDate.fromString(project_details[2], 'yyyy-MM-dd')
        self.dateEdit_2.setDate(start_date)
        end_date = QDate.fromString(project_details[3], 'yyyy-MM-dd')
        self.dateEdit_3.setDate(end_date)
        self.comboBox.setCurrentText(project_details[4])  # Assuming this is the client's name

        # Connect the update button to the update_project function
        self.pushButton.clicked.connect(self.update_project)

    def update_project(self):
        # Get the entered project information from the UI
        project_name = self.lineEdit.text()
        description = self.lineEdit_5.text()
        start_date = self.dateEdit_2.date().toString("yyyy-MM-dd")
        end_date = self.dateEdit_3.date().toString("yyyy-MM-dd")
        client_name = self.comboBox.currentText()  # Assuming this is the client's name

        # Retrieve the ClientID from the Client table
        client_id_query = "SELECT ClientID FROM Client WHERE ClientName = ?"
        try:
            self.cursor.execute(client_id_query, (client_name,))
            client_id_result = self.cursor.fetchone()

            if client_id_result:
                client_id = client_id_result[0]

                # Update the project information in the database using the original ProjectID
                project_query = """
                    UPDATE Project
                    SET ProjectName = ?, Description = ?, StartDate = ?, EndDate = ?, ClientID = ?
                    WHERE ProjectID = ?
                """
                self.cursor.execute(project_query, (project_name, description, start_date, end_date, client_id, self.project_id))
                self.connection.commit()
                QMessageBox.information(self, 'Success', 'Project updated successfully.')

                # Notify that the editing is complete
                self.editing_complete.emit()
            else:
                QMessageBox.warning(self, 'Error', 'Client not found.')
        except pyodbc.Error as e:
            print(f"Error in database operation: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred during the database operation.')

        self.close()
    


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
    def __init__(self, project_id, project_name):
        super().__init__()
        loadUi('task.ui', self)
        self.project_id = project_id
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
        
        self.populate_tasks_for_project(self.project_id)
        self.label_2.setText(project_name)

        # self.load_data_into_table()
        #print(project_id)
        
    def populate_tasks_for_project(self, project_id):

        try:
            # Query to retrieve tasks for a specific project
            query = """
                SELECT 
                TaskName, 
                Description, 
                StartDate, 
                EndDate, 
                (SELECT StatusName FROM TaskStatus TS WHERE TS.StatusID = Task.StatusID) AS StatusName,
                (SELECT Name FROM Users U WHERE U.UserID = Task.AssigneeID) AS Assigned
            FROM Task
            WHERE ProjectID = ?
            """
        
            # Execute the query with the specific project ID
            tasks = self.cursor.execute(query, (project_id,)).fetchall()

            # Set the number of rows in the tasks table
            self.tableWidget.setRowCount(len(tasks))

            # Populate the table with task details
            for row, task in enumerate(tasks):
                for col, value in enumerate(task):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row, col, item)

            # # Set the column headers for tasks
            # headers = ["Task ID", "Task Name", "Description", "Start Date", "End Date", "Status ID"]
            # self.tableWidget.setHorizontalHeaderLabels(headers)

        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while retrieving tasks for the project.')
            self.tableWidget.update()  # Refresh the UI


    # def load_data_into_table(self):
    #     # Clear the table first
    #     self.tableWidget.setRowCount(0)

    #     # Define your query to fetch data
    #     query = "SELECT TaskName, Description, StartDate, EndDate, StatusName as Status FROM Task T join TaskStatus TS on T.StatusID = TS.StatusID"
    #     try:
    #         self.cursor.execute(query)
    #         for row_number, row_data in enumerate(self.cursor):
    #             # print(f"Row {row_number}: {row_data}")  # Debugging line
    #             self.tableWidget.insertRow(row_number)
    #             for column_number, data in enumerate(row_data):
    #                 # print(f"Column {column_number}: {data}")  # Debugging line
    #                 self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    #     except pyodbc.Error as e:
    #         print(f"Error loading data into table: {e}")
    #         QMessageBox.warning(self, 'Database Error', 'An error occurred while loading data into the table.')

    #     self.tableWidget.update()  # Refresh the UI

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
        self.pushButton.clicked.connect(self.save_task)
        self.populate_department_combo_box()

    def populate_department_combo_box(self):
        query = "SELECT U.UserID, U.Name, R.RoleName FROM Users U JOIN Role R ON U.RoleID = R.RoleID"
        try:
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            for user in users:
                user_id = user[0]
                user_name = user[1]
                user_role = user[2]
                combo_text = f"{user_name} - {user_role}"
                self.comboBox.addItem(combo_text, user_id)  # Adding user_id as userData
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            QMessageBox.warning(self, 'Database Error', 'An error occurred while retrieving data.')


    def save_task(self):
        # Get the entered task information from the UI
        task_name = self.lineEdit.text()
        description = self.lineEdit_5.text()
        start_date = self.dateEdit_2.date().toString("yyyy-MM-dd")
        end_date = self.dateEdit.date().toString("yyyy-MM-dd")
        # assigned_to = self.comboBox.currentText()

        assigned_to_user_id = self.comboBox.currentData()  # Get the userID from the selected combo box item

        query = "INSERT INTO Task (TaskName, Description, StartDate, EndDate, AssigneeID) VALUES (?, ?, ?, ?, ?)"
        try:
            self.cursor.execute(query, task_name, description, start_date, end_date, assigned_to_user_id)
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


