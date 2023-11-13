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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
