from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt


class GradientButton(QPushButton):
    def __init__(self, text, color_scheme, parent=None):
        super().__init__(text, parent)
        self.color_scheme = color_scheme
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(160, 50)
        self.setFont(QFont("Segoe UI", 12, QFont.Bold))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(2, 2, self.width()-4, self.height()-4, 12, 12)

        gradient = QLinearGradient(0, 0, 0, self.height())

        if self.isEnabled():
            if self.underMouse():
                gradient.setColorAt(0, self.color_scheme["hover_top"])
                gradient.setColorAt(1, self.color_scheme["hover_bottom"])
            else:
                gradient.setColorAt(0, self.color_scheme["normal_top"])
                gradient.setColorAt(1, self.color_scheme["normal_bottom"])
        else:
            gradient.setColorAt(0, QColor("#D3D3D3"))
            gradient.setColorAt(1, QColor("#C0C0C0"))

        painter.fillPath(path, gradient)

        painter.setPen(QColor(self.color_scheme["text"]))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class HomeWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.welcome_label = None

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#F8F6FF"))
        gradient.setColorAt(1, QColor("#E6E6FA"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 40, 30, 40)
        main_layout.setSpacing(25)

        self.welcome_label = QLabel("Welcome!")
        self.welcome_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("""
            color: #4B0082;
            background: transparent;
            padding: 10px;
            margin-bottom: 5px;
        """)
        main_layout.addWidget(self.welcome_label)

        subtitle_label = QLabel("What would you like to do?")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(
            "color: #6A5ACD; background: transparent; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)

        button_container = QWidget()
        button_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.6);
            border-radius: 16px;
            border: 1px solid rgba(177, 156, 217, 0.3);
        """)
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(20, 25, 20, 25)
        button_layout.setSpacing(20)

        new_chat_colors = {
            "normal_top": QColor("#9370DB"),
            "normal_bottom": QColor("#7B68EE"),
            "hover_top": QColor("#A891D6"),
            "hover_bottom": QColor("#9370DB"),
            "text": "#FFFFFF"
        }

        existing_chats_colors = {
            "normal_top": QColor("#6A5ACD"),
            "normal_bottom": QColor("#5C4AA8"),
            "hover_top": QColor("#7B68EE"),
            "hover_bottom": QColor("#6A5ACD"),
            "text": "#FFFFFF"
        }

        logout_colors = {
            "normal_top": QColor("#D8BFD8"),
            "normal_bottom": QColor("#C7A4C7"),
            "hover_top": QColor("#E6E6FA"),
            "hover_bottom": QColor("#D8BFD8"),
            "text": "#4B0082"
        }

        newChatButton = GradientButton("Start New Chat", new_chat_colors, self)
        newChatButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        newChatButton.clicked.connect(self.parent.show_new_chat)
        button_layout.addWidget(newChatButton, alignment=Qt.AlignCenter)

        existingChatsButton = GradientButton(
            "My Conversations", existing_chats_colors, self)
        existingChatsButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        existingChatsButton.clicked.connect(
            self.parent.show_existing_chats_list)
        button_layout.addWidget(existingChatsButton, alignment=Qt.AlignCenter)

        logoutButton = GradientButton("Logout", logout_colors, self)
        logoutButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        logoutButton.clicked.connect(self.logout)
        button_layout.addWidget(logoutButton, alignment=Qt.AlignCenter)

        main_layout.addWidget(button_container)

        decoration = QLabel("💬")
        decoration.setAlignment(Qt.AlignCenter)
        decoration.setFont(QFont("Segoe UI", 24))
        decoration.setStyleSheet(
            "color: #B19CD9; background: transparent; margin-top: 20px;")
        main_layout.addWidget(decoration)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def showEvent(self, event):
        """Override showEvent to update the username when the window is shown"""
        super().showEvent(event)
        self.update_welcome_message()

    def update_welcome_message(self):
        """Update the welcome message with the current username"""
        username = self.parent.get_username()
        if username:
            self.welcome_label.setText(f"Welcome, {username}!")
        else:
            self.welcome_label.setText("Welcome!")

    def logout(self):
        self.parent.set_username("")
        self.parent.show_menu()
