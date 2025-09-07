from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPalette
from PyQt5.QtCore import Qt
import requests
import json
from utils.ip_utils import get_local_ip
from config.config import SERVER


class RoundedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 44)
        self.setFont(QFont("Segoe UI", 10))

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)

        if self.hasFocus():
            painter.setPen(QColor("#7B68EE"))
            painter.setBrush(Qt.NoBrush)
        else:
            painter.setPen(QColor("#D8BFD8"))
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


class SignupWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#F5F0FF"))  # Very light lavender
        gradient.setColorAt(1, QColor("#E6E6FA"))  # Lavender
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title_label = QLabel("Create Account")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #4B0082;
            background: transparent;
            padding: 5px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)

        form_container = QWidget()
        form_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            border: 1px solid rgba(177, 156, 217, 0.3);
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        username_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        form_layout.addWidget(username_label)

        self.username_input = RoundedLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
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

        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        password_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        form_layout.addWidget(password_label)

        self.password_input = RoundedLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
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

        button_colors = {
            "normal_top": QColor("#7B68EE"),
            "normal_bottom": QColor("#6A5ACD"),
            "hover_top": QColor("#9370DB"),
            "hover_bottom": QColor("#7B68EE"),
            "text": "#FFFFFF"
        }

        signupButton = GradientButton("Create Account", button_colors, self)
        signupButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        signupButton.clicked.connect(self.signup)
        main_layout.addWidget(signupButton, alignment=Qt.AlignCenter)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def signup(self):
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
            uri = f"{SERVER}/api/users/register"
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
                self.username_input.clear()
                self.password_input.clear()
                self.username_error.setText("")
                self.password_error.setText("✓ Account created successfully!")
                self.password_error.setStyleSheet(
                    "color: #2E8B57; background: transparent;")
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
