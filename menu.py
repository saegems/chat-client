from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MenuWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Create a layout for the menu
        layout = QVBoxLayout()
        # Reduced padding for better scaling
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)  # Slightly reduced spacing for consistency

        # Set consistent font with fallback
        # Smaller font size with fallback
        button_font = QFont("Segoe UI, Arial", 10)

        # Create and style the "Sign Up" button
        signupButton = QPushButton("Signup", self)
        signupButton.setMinimumSize(120, 40)  # Minimum size instead of fixed
        signupButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        signupButton.setFont(button_font)
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
        signupButton.clicked.connect(self.parent.show_signup)
        layout.addWidget(signupButton, alignment=Qt.AlignCenter)

        # Create and style the "Login" button
        loginButton = QPushButton("Login", self)
        loginButton.setMinimumSize(120, 40)  # Minimum size instead of fixed
        loginButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loginButton.setFont(button_font)
        loginButton.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; /* Blue for secondary action */
                color: white;
                border-radius: 6px; /* Slightly larger for high-DPI */
                padding: 8px; /* Adjusted for scaling */
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
