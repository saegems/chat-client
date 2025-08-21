from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class ChatListItem(QWidget):
    def __init__(self, username, message, time, parent=None):
        super().__init__(parent)

        username_font = QFont("Segoe UI, Arial", 12, QFont.Bold)
        message_font = QFont("Segoe UI, Arial", 10)
        time_font = QFont("Segoe UI, Arial", 8)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(5)

        username_label = QLabel(username)
        username_label.setFont(username_font)
        username_label.setStyleSheet("color: #4B0082;")
        username_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(username_label)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        message_label = QLabel(message)
        message_label.setFont(message_font)
        message_label.setStyleSheet("color: #4B0082;")
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setWordWrap(True)
        bottom_layout.addWidget(message_label, stretch=1)

        time_label = QLabel(time)
        time_label.setFont(time_font)
        time_label.setStyleSheet("color: #9370DB;")
        time_label.setAlignment(Qt.AlignRight)
        bottom_layout.addWidget(time_label)

        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        self.setStyleSheet("background-color: #FFF0F5; border-radius: 5px;")
