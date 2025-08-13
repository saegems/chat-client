from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MenuWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Create a layout for the menu
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Add padding
        layout.setSpacing(20)  # Increase spacing for better separation

        # Create and style the "Sign Up" button
        signupButton = QPushButton("Signup", self)
        signupButton.setFixedWidth(100)  # Wider for better proportions
        signupButton.setFixedHeight(40)
        signupButton.setFont(QFont("Segoe UI", 12))
        signupButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green for primary action */
                color: white;
                border-radius: 5px; /* Rounded corners */
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #66BB6A; /* Lighter green on hover */
            }
        """)
        signupButton.clicked.connect(self.parent.show_signup)
        layout.addWidget(signupButton, alignment=Qt.AlignCenter)

        # Create and style the "Login" button
        loginButton = QPushButton("Login", self)
        loginButton.setFixedWidth(100)
        loginButton.setFixedHeight(40)
        loginButton.setFont(QFont("Segoe UI", 12))
        loginButton.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; /* Blue for secondary action */
                color: white;
                border-radius: 5px; /* Rounded corners */
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #42A5F5; /* Lighter blue on hover */
            }
        """)
        loginButton.clicked.connect(self.parent.show_login)
        layout.addWidget(loginButton, alignment=Qt.AlignCenter)

        # Add stretch to push content to top
        layout.addStretch()

        # Set the layout for the widget
        self.setLayout(layout)
