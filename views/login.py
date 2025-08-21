from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPalette
from PyQt5.QtCore import Qt
import requests
import json
from utils.ip_utils import get_local_ip


class RoundedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 44)
        self.setFont(QFont("Segoe UI", 10))

    def paintEvent(self, event):
        # Let the base class handle the text rendering
        super().paintEvent(event)

        # Draw rounded border
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # Create rounded rectangle path for border
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)

        # Draw border based on focus state
        if self.hasFocus():
            painter.setPen(QColor("#FF69B4"))  # Pink border when focused
            painter.setBrush(Qt.NoBrush)
        else:
            painter.setPen(QColor("#FFB6C1"))  # Light pink border
            painter.setBrush(Qt.NoBrush)

        painter.drawPath(path)


class GradientButton(QPushButton):
    def __init__(self, text, color_scheme, parent=None):
        super().__init__(text, parent)
        self.color_scheme = color_scheme
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(140, 48)
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


class LoginWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # Set background with subtle gradient
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#FFF0F5"))  # Very light pink
        gradient.setColorAt(1, QColor("#FFE4E9"))  # Light pink
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Title with improved styling
        title_label = QLabel("Welcome Back")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #4B0082;
            background: transparent;
            padding: 5px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Sign in to continue chatting")
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(
            "color: #9370DB; background: transparent; margin-bottom: 15px;")
        main_layout.addWidget(subtitle_label)

        # Form container with subtle border
        form_container = QWidget()
        form_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            border: 1px solid rgba(255, 182, 193, 0.3);
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # Username section
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        username_label.setStyleSheet(
            "color: #FF69B4; background: transparent;")
        form_layout.addWidget(username_label)

        self.username_input = RoundedLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #FFB6C1;
            }
        """)
        form_layout.addWidget(self.username_input)

        self.username_error = QLabel("")
        self.username_error.setFont(QFont("Segoe UI", 9))
        self.username_error.setStyleSheet(
            "color: #FF4500; background: transparent;")
        self.username_error.setAlignment(Qt.AlignLeft)
        self.username_error.setWordWrap(True)
        form_layout.addWidget(self.username_error)

        # Password section
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        password_label.setStyleSheet(
            "color: #FF69B4; background: transparent;")
        form_layout.addWidget(password_label)

        self.password_input = RoundedLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #FFB6C1;
            }
        """)
        form_layout.addWidget(self.password_input)

        self.password_error = QLabel("")
        self.password_error.setFont(QFont("Segoe UI", 9))
        self.password_error.setStyleSheet(
            "color: #FF4500; background: transparent;")
        self.password_error.setAlignment(Qt.AlignLeft)
        self.password_error.setWordWrap(True)
        form_layout.addWidget(self.password_error)

        main_layout.addWidget(form_container)

        # Login button with gradient
        button_colors = {
            "normal_top": QColor("#FF69B4"),
            "normal_bottom": QColor("#FF1493"),
            "hover_top": QColor("#FFB6C1"),
            "hover_bottom": QColor("#FF69B4"),
            "text": "#FFFFFF"
        }

        loginButton = GradientButton("Sign In", button_colors, self)
        loginButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loginButton.clicked.connect(self.login)
        main_layout.addWidget(loginButton, alignment=Qt.AlignCenter)

        # Add some spacing at the bottom
        main_layout.addStretch()

        self.setLayout(main_layout)

    def login(self):
        self.username_error.setText("")
        self.password_error.setText("")
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        ip = get_local_ip()
        if not username:
            self.username_error.setText("Username cannot be empty.")
            return
        if not password:
            self.password_error.setText("Password cannot be empty.")
            return
        data = {
            "username": username,
            "password": password,
            "ip": ip
        }

        try:
            uri = "http://127.0.0.1:8080/api/users/login"
            response = requests.post(uri, json=data, timeout=5)
            response.raise_for_status()
            response_data = {}

            if response.content:
                try:
                    response_data = response.json()
                    print(response_data)
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
            else:
                print("No body received")

            if response.status_code == 200:
                self.parent.set_username(username)
                self.username_input.clear()
                self.password_input.clear()
                self.username_error.setText("")
                self.password_error.setText("✓ Login successful!")
                self.password_error.setStyleSheet(
                    "color: #2E8B57; background: transparent;")
                self.parent.show_home()
            else:
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.username_error.setText(error.get("username", ""))
                    self.password_error.setText(error.get("password", ""))
                else:
                    self.username_error.setText(error)

        except requests.exceptions.RequestException as e:
            self.username_error.setText("Network error")
            self.password_error.setText(str(e))
        except json.JSONDecodeError:
            self.username_error.setText("Invalid response from server")
            self.password_error.setText("")
