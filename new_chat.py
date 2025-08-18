from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtGui import QTextOption
from PyQt5.QtCore import Qt
import requests
import json


class NewChatWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Set gradient background
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 500)  # Match 400x500 window
        gradient.setColorAt(0, QColor("#1e1e2e"))
        gradient.setColorAt(1, QColor("#3b3b4f"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        self.input_font = QFont("Segoe UI, Arial", 10)
        self.button_font = QFont("Segoe UI, Arial", 12)
        self.error_font = QFont("Segoe UI, Arial", 8)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        top_layout = QHBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setMinimumSize(200, 40)
        self.username_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.username_input.setFont(self.input_font)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a3a;
                color: #e0e0e0;
                border: 1px solid #4a4a5a;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #66BB6A;
            }
        """)
        top_layout.addWidget(self.username_input)

        find_button = QPushButton("Find")
        find_button.setMinimumSize(100, 40)
        find_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        find_button.setFont(self.button_font)
        find_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #42A5F5;
            }
        """)
        find_button.clicked.connect(self.find_user)
        top_layout.addWidget(find_button, alignment=Qt.AlignCenter)

        self.main_layout.addLayout(top_layout)

        self.error_message = QLabel("")
        self.error_message.setFont(self.error_font)
        self.error_message.setStyleSheet("color: #ff5555;")
        self.error_message.setAlignment(Qt.AlignLeft)
        self.main_layout.addWidget(self.error_message)

        self.message_input = QTextEdit()
        self.message_input.setMinimumSize(200, 100)
        self.message_input.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.message_input.setFont(self.input_font)
        self.message_input.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.message_input.setLineWrapMode(QTextEdit.WidgetWidth)
        self.message_input.setWordWrapMode(
            QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.message_input.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a3a;
                color: #e0e0e0;
                border: 1px solid #4a4a5a;
                padding: 6px;
            }
            QTextEdit:focus {
                border: 1px solid #66BB6A;
            }
        """)
        self.message_input.setDisabled(True)
        self.main_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.setMinimumSize(100, 40)
        self.send_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.send_button.setFont(self.button_font)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
        """)
        # self.send_button.clicked.connect(self.send_message)
        self.send_button.setVisible(False)  # Hidden until change_view
        self.main_layout.addWidget(self.send_button, alignment=Qt.AlignRight)

        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def change_view(self):
        """Enable message input and show Send button."""
        self.error_message.setText("")
        self.message_input.setDisabled(False)
        self.send_button.setVisible(True)

    def find_user(self):
        """Search for a user via API and switch to chat view if found."""
        self.error_message.setText("")
        username = self.username_input.text().strip()
        if not username:
            self.error_message.setText("Username cannot be empty")
            self.message_input.setDisabled(True)
            self.send_button.setVisible(False)
            return

        try:
            uri = "http://127.0.0.1:8080/api/users"
            params = {"username": username}
            response = requests.get(uri, params=params, timeout=5)
            response.raise_for_status()

            try:
                response_data = response.json()
            except json.JSONDecodeError:
                self.error_message.setText("Invalid response from server")
                self.message_input.setDisabled(True)
                self.send_button.setVisible(False)
                return

            if response.status_code == 200:
                self.change_view()
            else:
                self.message_input.setDisabled(True)
                self.send_button.setVisible(False)
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.error_message.setText(error.get("username", ""))
                else:
                    self.error_message.setText(error)

        except requests.exceptions.RequestException as e:
            self.error_message.setText(f"Network error: {str(e)}")
            self.message_input.setDisabled(True)
            self.send_button.setVisible(False)
