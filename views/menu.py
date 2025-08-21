from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MenuWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        button_font = QFont("Segoe UI, Arial", 10)

        signupButton = QPushButton("Signup", self)
        signupButton.setMinimumSize(120, 40)
        signupButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        signupButton.setFont(button_font)
        signupButton.setStyleSheet("""
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
        signupButton.clicked.connect(self.parent.show_signup)
        layout.addWidget(signupButton, alignment=Qt.AlignCenter)

        loginButton = QPushButton("Login", self)
        loginButton.setMinimumSize(120, 40)
        loginButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loginButton.setFont(button_font)
        loginButton.setStyleSheet("""
            QPushButton {
                background-color: #FF69B4; /* Pink */
                color: #4B0082; /* Dark purple */
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #FFB6C1; /* Light pink */
            }
        """)
        loginButton.clicked.connect(self.parent.show_login)
        layout.addWidget(loginButton, alignment=Qt.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)
