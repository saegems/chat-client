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

        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(2, 2, self.width()-4, self.height()-4, 12, 12)

        # Create gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())

        if self.isEnabled():
            if self.underMouse():
                # Hover state gradient
                gradient.setColorAt(0, self.color_scheme["hover_top"])
                gradient.setColorAt(1, self.color_scheme["hover_bottom"])
            else:
                # Normal state gradient
                gradient.setColorAt(0, self.color_scheme["normal_top"])
                gradient.setColorAt(1, self.color_scheme["normal_bottom"])
        else:
            # Disabled state
            gradient.setColorAt(0, QColor("#D3D3D3"))
            gradient.setColorAt(1, QColor("#C0C0C0"))

        painter.fillPath(path, gradient)

        # Draw text
        painter.setPen(QColor(self.color_scheme["text"]))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class HomeWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Set background with subtle gradient
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#F8F6FF"))  # Very light lavender
        gradient.setColorAt(1, QColor("#E6E6FA"))  # Lavender
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 40, 30, 40)
        main_layout.setSpacing(25)

        # Welcome message with username
        welcome_label = QLabel(f"Welcome, {self.parent.get_username()}!")
        welcome_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            color: #4B0082;
            background: transparent;
            padding: 10px;
            margin-bottom: 5px;
        """)
        main_layout.addWidget(welcome_label)

        # Subtitle
        subtitle_label = QLabel("What would you like to do?")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(
            "color: #6A5ACD; background: transparent; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)

        # Button container with subtle styling
        button_container = QWidget()
        button_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.6);
            border-radius: 16px;
            border: 1px solid rgba(177, 156, 217, 0.3);
        """)
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(20, 25, 20, 25)
        button_layout.setSpacing(20)

        # Define color schemes for buttons
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

        # New Chat button
        newChatButton = GradientButton("Start New Chat", new_chat_colors, self)
        newChatButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        newChatButton.clicked.connect(self.parent.show_new_chat)
        button_layout.addWidget(newChatButton, alignment=Qt.AlignCenter)

        # Existing Chats button
        existingChatsButton = GradientButton(
            "My Conversations", existing_chats_colors, self)
        existingChatsButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        existingChatsButton.clicked.connect(
            self.parent.show_existing_chats_list)
        button_layout.addWidget(existingChatsButton, alignment=Qt.AlignCenter)

        # Logout button
        logoutButton = GradientButton("Logout", logout_colors, self)
        logoutButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button_layout.addWidget(logoutButton, alignment=Qt.AlignCenter)

        main_layout.addWidget(button_container)

        # Decorative element
        decoration = QLabel("💬")
        decoration.setAlignment(Qt.AlignCenter)
        decoration.setFont(QFont("Segoe UI", 24))
        decoration.setStyleSheet(
            "color: #B19CD9; background: transparent; margin-top: 20px;")
        main_layout.addWidget(decoration)

        # Add some spacing at the bottom
        main_layout.addStretch()

        self.setLayout(main_layout)
