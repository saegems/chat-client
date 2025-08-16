from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt
import requests
import json
from utils.ip_utils import get_local_ip


class SignupWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Set gradient background to match MainWindow
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#1e1e2e"))  # Dark top
        gradient.setColorAt(1, QColor("#3b3b4f"))  # Lighter bottom
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # Create a layout for the signup form
        main_layout = QVBoxLayout()
        # Reduced padding for better scaling
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)  # Slightly reduced spacing for consistency

        # Set consistent font with fallback
        label_font = QFont("Segoe UI, Arial", 14,
                           QFont.Bold)  # Smaller title font
        input_font = QFont("Segoe UI, Arial", 10)  # Smaller input font
        error_font = QFont("Segoe UI, Arial", 8)  # Smaller error font

        # Create and style the "Sign Up" label
        label = QLabel("Signup")
        label.setFont(label_font)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        label.setStyleSheet("color: #e0e0e0;")
        main_layout.addWidget(label)

        # Create username input field
        username_label = QLabel("Username")
        username_label.setFont(input_font)
        username_label.setStyleSheet("color: #e0e0e0;")
        main_layout.addWidget(username_label)

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
                border: 1px solid #4a4a5a;
                border-radius: 6px; /* Slightly larger for high-DPI */
                padding: 6px; /* Adjusted for scaling */
            }
            QLineEdit:focus {
                border: 1px solid #66BB6A; /* Green border on focus */
            }
        """)
        main_layout.addWidget(self.username_input)

        # Create username error label
        self.username_error = QLabel("")
        self.username_error.setFont(error_font)
        self.username_error.setStyleSheet(
            "color: #ff5555;")  # Red for error text
        self.username_error.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.username_error)

        # Create password input field
        password_label = QLabel("Password")
        password_label.setFont(input_font)
        password_label.setStyleSheet("color: #e0e0e0;")
        main_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setMinimumSize(
            200, 40)  # Minimum size for scalability
        self.password_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.password_input.setFont(input_font)
        self.password_input.setEchoMode(QLineEdit.Password)  # Mask password
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a3a;
                color: #e0e0e0;
                border: 1px solid #4a4a5a;
                border-radius: 6px; /* Slightly larger for high-DPI */
                padding: 6px; /* Adjusted for scaling */
            }
            QLineEdit:focus {
                border: 1px solid #66BB6A; /* Green border on focus */
            }
        """)
        main_layout.addWidget(self.password_input)

        # Create password error label
        self.password_error = QLabel("")
        self.password_error.setFont(error_font)
        self.password_error.setStyleSheet(
            "color: #ff5555;")  # Red for error text
        self.password_error.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.password_error)

        # Create and style the "Sign Up" button
        signupButton = QPushButton("Signup")
        signupButton.setMinimumSize(120, 40)  # Minimum size instead of fixed
        signupButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        signupButton.setFont(input_font)
        signupButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green for primary action */
                color: white;
                border-radius: 6px; /* Slightly larger for high-DPI */
                padding: 8px; /* Adjusted for scaling */
            }
            QPushButton:hover {
                background-color: #66BB6A; /* Lighter green on hover */
            }
        """)
        signupButton.clicked.connect(self.signup)
        main_layout.addWidget(signupButton, alignment=Qt.AlignCenter)

        # Add stretch to push content to top
        main_layout.addStretch()

        # Set the layout for the widget
        self.setLayout(main_layout)

    def signup(self):
        self.username_error.setText("")
        self.password_error.setText("")
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        ip = get_local_ip()
        if not username:
            self.username_error.setText("Username cannot be empty.")
            return
        if not password:
            self.password_error.setText("Password cannot be empty.")
            return
        data = {
            "username": username,
            "password": password,
            "ip": ip
        }

        try:
            uri = "http://127.0.0.1:8080/api/users/register"
            response = requests.post(uri, json=data, timeout=5)
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
                self.username_input.clear()
                self.password_input.clear()
                self.username_error.setText("")
                self.password_error.setText("Signup successful!")
            else:
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.username_error.setText(error.get("username", ""))
                    self.password_error.setText(error.get("password", ""))
                else:
                    self.username_error.setText(error)

        except requests.exceptions.RequestException as e:
            self.username_error.setText("Network error")
            self.password_error.setText(str(e))
        except json.JSONDecodeError:
            self.username_error.setText("Invalid response from server")
            self.password_error.setText("")
