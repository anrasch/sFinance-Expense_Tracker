import sys
import os
import sqlite3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QTextEdit, QMessageBox, QApplication)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPalette, QColor, QIntValidator

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Database setup
conn = sqlite3.connect('data/expenses.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    comment TEXT
                )''')
conn.commit()

# Main App class
class SFinanceApp(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window  # Store reference to main window

        self.setWindowTitle("sFinance - Add Expense")
        self.setGeometry(100, 100, 400, 400)

        # Set gray background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(50, 50, 50))  # Dark gray
        self.setPalette(palette)

        # Layout
        layout = QVBoxLayout()

        # Labels and Input Fields with iOS-like style
        self.description_label = QLabel("Expense Description:")
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter description")
        
        self.category_label = QLabel("Category:")
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Food", "Transport", "Entertainment", "Health", "Utilities", "Other"])

        # Ensure black text in the dropdown
        self.category_input.setStyleSheet("""
            QComboBox {
                color: black;  /* Black text when closed */
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;  /* Black text in dropdown list */
            }
        """)

        self.date_label = QLabel("Date:")
        self.date_input = QLineEdit(self)
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.date_input.setText(QDate.currentDate().toString("yyyy-MM-dd"))  # Set current date as default

        # Amount field with integer validation (allows only numbers)
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setValidator(QIntValidator(0, 1000000, self))  # Only allows numeric input

        self.comment_label = QLabel("Comment (Optional):")
        self.comment_input = QTextEdit(self)
        self.comment_input.setPlaceholderText("Enter additional notes")

        # Button to add expense
        self.submit_button = QPushButton("Add Expense")
        self.submit_button.clicked.connect(self.add_expense)

        # Back button to return to the main window
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back_to_main)

        # Add widgets to layout
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.back_button)  # Add the Back button

        self.setLayout(layout)

        # Apply stylesheet
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
                color: white;
            }
            QLineEdit, QComboBox, QTextEdit {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 8px;
                color: black;  /* Black text for input fields */
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005BBB;
            }
        """)

    def add_expense(self):
        description = self.description_input.text()
        category = self.category_input.currentText()
        date = self.date_input.text()  # Use text input for date
        amount = self.amount_input.text()
        comment = self.comment_input.toPlainText()

        if description and amount:
            try:
                amount = float(amount)
                # Insert into the database
                cursor.execute("INSERT INTO expenses (description, category, date, amount, comment) VALUES (?, ?, ?, ?, ?)", 
                               (description, category, date, amount, comment))
                conn.commit()
                QMessageBox.information(self, "Success", "Expense added successfully!")

                # Clear input fields
                self.description_input.clear()
                self.amount_input.clear()
                self.comment_input.clear()
                self.date_input.setText(QDate.currentDate().toString("yyyy-MM-dd"))  # Reset date to current

            except ValueError:
                QMessageBox.warning(self, "Error", "Please enter a valid amount.")
        else:
            QMessageBox.warning(self, "Error", "Please fill out all fields.")

    def go_back_to_main(self):
        self.close()  # Close the add expense window
        self.main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SFinanceApp(None)  # For standalone testing, pass None for the main window
    main_window.show()
    sys.exit(app.exec())
