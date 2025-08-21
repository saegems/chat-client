from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt


class HomeWindow(QWidget):
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

        button_font = QFont("Segoe UI, Arial", 10)

        newChatButton = QPushButton("New Chat")
        newChatButton.setMinimumSize(120, 40)
        newChatButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        newChatButton.setFont(button_font)
        newChatButton.setStyleSheet("""
            QPushButton {
                background-color: #E6E6FA; /* Lavender */
                color: #4B0082; /* Dark purple */
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #DDA0DD; /* Mauve */
            }
        """)
        newChatButton.clicked.connect(self.parent.show_new_chat)
        main_layout.addWidget(newChatButton, alignment=Qt.AlignCenter)

        existingChatsButton = QPushButton("Existing Chats")
        existingChatsButton.setMinimumSize(120, 40)
        existingChatsButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        existingChatsButton.setFont(button_font)
        existingChatsButton.setStyleSheet("""
            QPushButton {
                background-color: #E6E6FA; /* Lavender */
                color: #4B0082; /* Dark purple */
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #DDA0DD; /* Mauve */
            }
        """)
        main_layout.addWidget(existingChatsButton, alignment=Qt.AlignCenter)

        logoutButton = QPushButton("Logout")
        logoutButton.setMinimumSize(120, 40)
        logoutButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        logoutButton.setFont(button_font)
        logoutButton.setStyleSheet("""
            QPushButton {
                background-color: #E6E6FA; /* Lavender */
                color: #4B0082; /* Dark purple */
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #DDA0DD; /* Mauve */
            }
        """)
        main_layout.addWidget(logoutButton, alignment=Qt.AlignCenter)

        main_layout.addStretch()
        self.setLayout(main_layout)
