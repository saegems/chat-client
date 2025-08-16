from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt


class HomeWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#1e1e2e"))  # Dark top
        gradient.setColorAt(1, QColor("#3b3b4f"))  # Lighter bottom
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # Create a layout for the home window
        main_layout = QVBoxLayout()
        # Reduced padding for better scaling
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)  # Slightly reduced spacing for consistency

        # Set consistent font with fallback
        button_font = QFont("Segoe UI, Arial", 10)

        # Create and style the "New Chat" button
        newChatButton = QPushButton("New Chat")
        newChatButton.setMinimumSize(120, 40)  # Minimum size instead of fixed
        newChatButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        newChatButton.setFont(button_font)
        newChatButton.setStyleSheet("""
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
        # newChatButton.clicked.connect()
        main_layout.addWidget(newChatButton, alignment=Qt.AlignCenter)

        # Create and style the "Existing Chats" button
        existingChatsButton = QPushButton("Existing Chats")
        existingChatsButton.setMinimumSize(
            120, 40)  # Minimum size instead of fixed
        existingChatsButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        existingChatsButton.setFont(button_font)
        existingChatsButton.setStyleSheet("""
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
        # existingChatsButton.clicked.connect()
        main_layout.addWidget(existingChatsButton, alignment=Qt.AlignCenter)

        # Create and style the "Logout" button
        logoutButton = QPushButton("Logout")
        logoutButton.setMinimumSize(120, 40)  # Minimum size instead of fixed
        logoutButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        logoutButton.setFont(button_font)
        logoutButton.setStyleSheet("""
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
        # logoutButton.clicked.connect()
        main_layout.addWidget(logoutButton, alignment=Qt.AlignCenter)

        # Add stretch to push content to top
        main_layout.addStretch()

        # Set the layout for the widget
        self.setLayout(main_layout)
