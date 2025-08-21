from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt
import requests
import json
from utils.ip_utils import get_local_ip


class LoginWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#E6E6FA"))  # Lavender top
        gradient.setColorAt(1, QColor("#D8BFD8"))  # Mauve bottom
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        label_font = QFont("Segoe UI, Arial", 14, QFont.Bold)
        input_font = QFont("Segoe UI, Arial", 10)
        error_font = QFont("Segoe UI, Arial", 8)

        label = QLabel("Login")
        label.setFont(label_font)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        label.setStyleSheet("color: #4B0082;")  # Dark purple
        main_layout.addWidget(label)

        username_label = QLabel("Username")
        username_label.setFont(input_font)
        username_label.setStyleSheet("color: #4B0082;")  # Dark purple
        main_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setMinimumSize(200, 40)
        self.username_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.username_input.setFont(input_font)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFF0F5; /* Light pink */
                color: #4B0082; /* Dark purple */
                border: 1px solid #9370DB; /* Soft purple */
                border-radius: 6px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #BA55D3; /* Bright purple */
            }
        """)
        main_layout.addWidget(self.username_input)

        self.username_error = QLabel("")
        self.username_error.setFont(error_font)
        self.username_error.setStyleSheet("color: #FF4040;")  # Bright pink
        self.username_error.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.username_error)

        password_label = QLabel("Password")
        password_label.setFont(input_font)
        password_label.setStyleSheet("color: #4B0082;")  # Dark purple
        main_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setMinimumSize(200, 40)
        self.password_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.password_input.setFont(input_font)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFF0F5; /* Light pink */
                color: #4B0082; /* Dark purple */
                border: 1px solid #9370DB; /* Soft purple */
                border-radius: 6px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #BA55D3; /* Bright purple */
            }
        """)
        main_layout.addWidget(self.password_input)

        self.password_error = QLabel("")
        self.password_error.setFont(error_font)
        self.password_error.setStyleSheet("color: #FF4040;")  # Bright pink
        self.password_error.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.password_error)

        loginButton = QPushButton("Login")
        loginButton.setMinimumSize(120, 40)
        loginButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loginButton.setFont(input_font)
        loginButton.setStyleSheet("""
            QPushButton {
                background-color: #6495ED; /* Blue */
                color: #4B0082; /* Dark purple */
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #87CEFA; /* Light blue */
            }
        """)
        loginButton.clicked.connect(self.login)
        main_layout.addWidget(loginButton, alignment=Qt.AlignCenter)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def login(self):
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
            uri = "http://127.0.0.1:8080/api/users/login"
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
                self.parent.set_username(username)
                self.username_input.clear()
                self.password_input.clear()
                self.username_error.setText("")
                self.password_error.setText("Login successful!")
                self.parent.show_home()
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
