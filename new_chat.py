from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt
import requests
import json


class NewChatWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#1e1e2e"))  # Dark top
        gradient.setColorAt(1, QColor("#3b3b4f"))  # Lighter bottom
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        input_font = QFont("Segoe UI, Arial", 10)  # Smaller input font
        button_font = QFont("Segoe UI, Arial", 10)
        error_font = QFont("Segoe UI, Arial", 8)  # Smaller error font

        # Create a layout for the home window
        main_layout = QVBoxLayout()
        # Reduced padding for better scaling
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)  # Slightly reduced spacing for consistency

        top_layout = QHBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setMinimumSize(
            200, 40)  # Minimum size for scalability
        self.username_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.username_input.setFont(input_font)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a3a;
                color: #e0e0e0;
                padding: 6px; /* Adjusted for scaling */
            }
            QLineEdit:focus {
                border: 1px solid #66BB6A; /* Green border on focus */
            }
        """)
        top_layout.addWidget(self.username_input)

        findButton = QPushButton("Find")
        findButton.setMinimumSize(120, 40)  # Minimum size instead of fixed
        findButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        findButton.setFont(button_font)
        findButton.setStyleSheet("""
            QPushButton {
                background-color: #D2D8E3;
                color: black;
                border-radius: 6px; /* Slightly larger for high-DPI */
                padding: 8px; /* Adjusted for scaling */
            }
            QPushButton:hover {
                background-color: #C4E4E4;
            }
        """)
        findButton.clicked.connect(self.find_user)
        top_layout.addWidget(findButton, alignment=Qt.AlignCenter)

        main_layout.addLayout(top_layout)

        self.error_message = QLabel("")
        self.error_message.setFont(error_font)
        self.error_message.setStyleSheet(
            "color: #ff5555;")  # Red for error text
        self.error_message.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.error_message)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def find_user(self):
        self.error_message.setText("")
        username = self.username_input.text().strip()
        if not username:
            self.error_message.setText("Username cannot be empty.")
            return
        try:
            uri = f"http://127.0.0.1:8080/api/users"
            params = {
                "username": username
            }
            response = requests.get(uri, params=params, timeout=5)
            response.raise_for_status()
            response_data = {}

            if response.content:
                try:
                    response_data = response.json()
                    print(response_data)
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
            else:
                print("No body received")

            if response.status_code == 200:
                self.error_message.setText("")
            else:
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.error_message.setText(error.get("username", ""))
                else:
                    self.error_message.setText(error)
        except Exception as e:
            self.error_message.setText(str(e))
        return
