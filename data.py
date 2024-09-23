import sys
import sqlite3
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QDateEdit, 
                             QTableWidget, QTableWidgetItem, QApplication, QHBoxLayout)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPalette, QColor

# Database connection
conn = sqlite3.connect('data/expenses.db')
cursor = conn.cursor()

class DataEvaluationApp(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window  # Store reference to the main window

        self.setWindowTitle("sFinance - Data Evaluation")
        self.setGeometry(100, 100, 600, 400)

        # Set gray background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(50, 50, 50))  # Dark gray
        self.setPalette(palette)

        # Layout
        layout = QVBoxLayout()

        # Filter section
        filter_layout = QVBoxLayout()

        # Time filter
        self.time_filter_label = QLabel("Time Filter:")
        self.time_filter_combo = QComboBox(self)
        self.time_filter_combo.addItems(["Day", "Week", "Month", "Custom Range"])
        self.time_filter_combo.currentTextChanged.connect(self.update_time_filter_ui)

        # Date input fields for specific filters
        self.single_date_label = QLabel("Date:")
        self.single_date_input = QDateEdit(self)
        self.single_date_input.setCalendarPopup(True)
        self.single_date_input.setDate(QDate.currentDate())

        self.month_label = QLabel("Month:")
        self.month_input = QDateEdit(self)
        self.month_input.setCalendarPopup(True)
        self.month_input.setDate(QDate.currentDate())
        self.month_input.setDisplayFormat("MM/yyyy")

        self.start_date_label = QLabel("Start Date:")
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())

        self.end_date_label = QLabel("End Date:")
        self.end_date_input = QDateEdit(self)
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate())

        # Category filter
        self.category_label = QLabel("Category:")
        self.category_combo = QComboBox(self)
        self.load_categories()  # Load categories into the dropdown

        self.filter_button = QPushButton("Apply Filter")
        self.filter_button.clicked.connect(self.apply_filter)

        filter_layout.addWidget(self.time_filter_label)
        filter_layout.addWidget(self.time_filter_combo)
        filter_layout.addWidget(self.category_label)
        filter_layout.addWidget(self.category_combo)

        # Add all time-related widgets to the layout but hide them initially
        filter_layout.addWidget(self.single_date_label)
        filter_layout.addWidget(self.single_date_input)

        filter_layout.addWidget(self.month_label)
        filter_layout.addWidget(self.month_input)

        filter_layout.addWidget(self.start_date_label)
        filter_layout.addWidget(self.start_date_input)
        filter_layout.addWidget(self.end_date_label)
        filter_layout.addWidget(self.end_date_input)

        filter_layout.addWidget(self.filter_button)

        layout.addLayout(filter_layout)

        # Table to display expenses
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(5)
        self.expense_table.setHorizontalHeaderLabels(["Description", "Category", "Date", "Amount (€)", "Comment"])
        layout.addWidget(self.expense_table)

        # Label to display total sum
        self.total_label = QLabel("Total Sum: 0.00 €")
        layout.addWidget(self.total_label)

        # Back button to return to main window
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back_to_main)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        # Initialize with correct UI based on default filter
        self.update_time_filter_ui()

        # Apply the stylesheet for the design
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
                color: white;
            }
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                background-color: #f5f5f5;
                border-radius: 10px;
                padding: 8px;
                color: black;  /* Black text for input fields */
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;  /* Black text in dropdown menu */
            }
            QTableWidget {
                background-color: white;
                color: black;  /* Black text in table */
            }
            QTableWidget QHeaderView::section {
                background-color: #007AFF;
                color: white;  /* Header in blue with white text */
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

    def load_categories(self):
        """Load distinct categories from the database into the dropdown."""
        cursor.execute("SELECT DISTINCT category FROM expenses")
        categories = cursor.fetchall()
        self.category_combo.addItem("All Categories")  # Default option to show all categories
        for category in categories:
            self.category_combo.addItem(category[0])

    def update_time_filter_ui(self):
        """Update the UI to show relevant input fields based on selected time filter."""
        time_filter = self.time_filter_combo.currentText()

        # Hide all time input fields initially
        self.single_date_label.hide()
        self.single_date_input.hide()
        self.month_label.hide()
        self.month_input.hide()
        self.start_date_label.hide()
        self.start_date_input.hide()
        self.end_date_label.hide()
        self.end_date_input.hide()

        if time_filter == "Day":
            self.single_date_label.show()
            self.single_date_input.show()
        elif time_filter == "Week":
            self.single_date_label.show()  # Week is determined by a single date
            self.single_date_input.show()
        elif time_filter == "Month":
            self.month_label.show()
            self.month_input.show()
        elif time_filter == "Custom Range":
            self.start_date_label.show()
            self.start_date_input.show()
            self.end_date_label.show()
            self.end_date_input.show()

    def apply_filter(self):
        time_filter = self.time_filter_combo.currentText()
        category = self.category_combo.currentText()

        query = "SELECT description, category, date, amount, comment FROM expenses WHERE 1=1"
        params = []

        # Filter by time range
        if time_filter == "Day":
            date = self.single_date_input.date().toString("yyyy-MM-dd")
            query += " AND date = ?"
            params.append(date)
        elif time_filter == "Week":
            date = self.single_date_input.date().toString("yyyy-MM-dd")
            query += " AND strftime('%W', date) = strftime('%W', ?)"
            params.append(date)
        elif time_filter == "Month":
            month = self.month_input.date().toString("MM")
            year = self.month_input.date().toString("yyyy")
            query += " AND strftime('%m', date) = ? AND strftime('%Y', date) = ?"
            params.append(month)
            params.append(year)
        elif time_filter == "Custom Range":
            start_date = self.start_date_input.date().toString("yyyy-MM-dd")
            end_date = self.end_date_input.date().toString("yyyy-MM-dd")
            query += " AND date BETWEEN ? AND ?"
            params.append(start_date)
            params.append(end_date)

        # Filter by category (only if a specific category is selected)
        if category != "All Categories":
            query += " AND category = ?"
            params.append(category)

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Populate the table
        self.expense_table.setRowCount(0)  # Clear existing rows
        total_sum = 0

        for row_idx, row_data in enumerate(results):
            self.expense_table.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.expense_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            # Add the amount to the total sum
            total_sum += float(row_data[3])

        # Update the total sum label
        self.total_label.setText(f"Total Sum: {total_sum:.2f} €")

    def go_back_to_main(self):
        """Close the data evaluation window and return to the main window."""
        self.close()
        self.main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataEvaluationApp(None)  # For standalone testing, pass None for the main window
    window.show()
    sys.exit(app.exec())
