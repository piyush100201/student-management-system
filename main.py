import sys
import sqlite3

from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QToolBar, QStatusBar, \
    QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,600)


        #Add menu items
        file_menu_item = self.menuBar().addMenu("&File")

        help_menu_item = self.menuBar().addMenu("&Help")

        edit_menu_item = self.menuBar().addMenu("&Edit")


        #Add actions
        add_student_action = QAction(QIcon("icons/add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        #Add table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id","Name","Course","Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        #Create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        #Create status bar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        #Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)


    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)


        #Remove edit and delete widget if already present
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        #Add edit and delete widget
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("select * from students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology","Maths","Astronomy","Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        sms.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was added successfully.")
        confirmation_widget.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)



        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students where Name = ?",(name,))
        rows = list(result)
        print(rows)
        items = sms.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            sms.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
            super().__init__()
            self.setWindowTitle("Update Student Data")
            self.setFixedWidth(300)
            self.setFixedHeight(300)

            layout = QVBoxLayout()

            index = sms.table.currentRow()
            student_name = sms.table.item(index, 1).text()
            course_name = sms.table.item(index, 2).text()
            mobile = sms.table.item(index, 3).text()
            self.student_id = sms.table.item(index, 0).text()

            self.student_name = QLineEdit(student_name)
            self.student_name.setPlaceholderText("Name")
            layout.addWidget(self.student_name)

            self.course_name = QComboBox()
            courses = ["Biology", "Maths", "Astronomy", "Physics"]
            self.course_name.addItems(courses)
            self.course_name.setCurrentText(course_name)
            layout.addWidget(self.course_name)

            self.mobile = QLineEdit(mobile)
            self.mobile.setPlaceholderText("Mobile")
            layout.addWidget(self.mobile)

            button = QPushButton("Update")
            button.clicked.connect(self.update_student)
            layout.addWidget(button)

            self.setLayout(layout)

    def update_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        id = self.student_id
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (name, course, mobile, id))

        connection.commit()
        cursor.close()
        connection.close()
        sms.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was updated successfully.")
        confirmation_widget.exec()


class DeleteDialog(QDialog):
    def __init__(self):
            super().__init__()
            self.setWindowTitle("Delete Student Data")

            layout = QGridLayout()
            confirmation = QLabel("Are you sure you want to delete?")
            yes = QPushButton("Yes")
            no = QPushButton("No")

            layout.addWidget(confirmation, 0, 0, 1, 2)
            layout.addWidget(yes, 1,0)
            layout.addWidget(no, 1,1)

            index = sms.table.currentRow()
            self.student_id = sms.table.item(index, 0).text()

            yes.clicked.connect(self.delete_student)
            no.clicked.connect(self.close_delete_dialog)

            self.setLayout(layout)

    def delete_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE  from students WHERE id = ?",
                       (self.student_id,))

        connection.commit()
        cursor.close()
        connection.close()
        sms.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Record was deleted successfully.")
        confirmation_widget.exec()

    def close_delete_dialog(self):
        self.close()

class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = "This is student management system which allows user to add, edit and delete student data."
        self.setText(content)



app = QApplication(sys.argv)

sms = MainWindow()
sms.show()
sms.load_data()
sys.exit(app.exec())