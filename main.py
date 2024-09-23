import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPalette, QColor, QIcon
from sfinance import SFinanceApp
from data import DataEvaluationApp

# Funktion, um den Pfad zu Ressourcen zu finden, unabhängig davon, ob das Programm als Skript oder EXE ausgeführt wird
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller erstellt einen temporären Pfad zu den Ressourcen
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Create the data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Main window class
class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("sFinance - Main Menu")
        self.setGeometry(100, 100, 300, 200)

        # Setze das App-Icon, Pfad wird mit resource_path dynamisch gefunden
        self.setWindowIcon(QIcon(resource_path('assets/logo.png')))

        # Set gray background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(50, 50, 50))  # Dark gray
        self.setPalette(palette)

        # Layout
        layout = QVBoxLayout()

        # Buttons
        self.add_expense_button = QPushButton("Add Expense")
        self.add_expense_button.clicked.connect(self.open_add_expense_window)

        self.evaluate_data_button = QPushButton("Evaluate Data")
        self.evaluate_data_button.clicked.connect(self.open_evaluate_data_window)

        # Add buttons to layout
        layout.addWidget(self.add_expense_button)
        layout.addWidget(self.evaluate_data_button)

        self.setLayout(layout)

        # Apply the same stylesheet for buttons as in sFinanceApp
        self.setStyleSheet("""
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

    def open_add_expense_window(self):
        self.expense_window = SFinanceApp(self)  # Pass self (MainApp) as argument
        self.expense_window.show()
        self.hide()  # Hide the main window when opening the add expense window

    def open_evaluate_data_window(self):
        self.data_window = DataEvaluationApp(self)  # Pass self (MainApp) as the main window argument
        self.data_window.show()
        self.hide()  # Hide the main window when opening the data evaluation window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
