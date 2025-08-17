from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt


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

        main_layout.addLayout(top_layout)

        main_layout.addStretch()
        self.setLayout(main_layout)
