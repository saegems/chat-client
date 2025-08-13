from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt


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
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding
        main_layout.setSpacing(20)  # Increase spacing for better separation

        # Create and style the "Sign Up" label
        label = QLabel("Signup")
        # Consistent modern font
        label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        label.setStyleSheet("color: #e0e0e0;")  # Light gray for contrast
        main_layout.addWidget(label)

        # Create username input field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 12))
        username_label.setStyleSheet("color: #e0e0e0;")
        main_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(40)
        self.username_input.setFont(QFont("Segoe UI", 12))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a3a;
                color: #e0e0e0;
                border: 1px solid #4a4a5a;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #66BB6A; /* Green border on focus */
            }
        """)
        main_layout.addWidget(self.username_input)

        # Create username error label
        self.username_error = QLabel("")
        self.username_error.setFont(QFont("Segoe UI", 10))
        self.username_error.setStyleSheet(
            "color: #ff5555;")  # Red for error text
        self.username_error.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.username_error)

        # Create password input field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 12))
        password_label.setStyleSheet("color: #e0e0e0;")
        main_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(40)
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.setEchoMode(QLineEdit.Password)  # Mask password
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a3a;
                color: #e0e0e0;
                border: 1px solid #4a4a5a;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #66BB6A; /* Green border on focus */
            }
        """)
        main_layout.addWidget(self.password_input)

        # Create password error label
        self.password_error = QLabel("")
        self.password_error.setFont(QFont("Segoe UI", 10))
        self.password_error.setStyleSheet(
            "color: #ff5555;")  # Red for error text
        self.password_error.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(self.password_error)

        # Create and style the "Sign Up" button
        signupButton = QPushButton("Signup")
        signupButton.setFixedWidth(100)  # Consistent with MenuWindow
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
        main_layout.addWidget(signupButton, alignment=Qt.AlignCenter)

        # Add stretch to push content to top
        main_layout.addStretch()

        # Set the layout for the widget
        self.setLayout(main_layout)
