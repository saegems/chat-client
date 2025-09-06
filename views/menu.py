from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve


class RoundedButton(QPushButton):
    def __init__(self, text, color_scheme, parent=None):
        super().__init__(text, parent)
        self.color_scheme = color_scheme
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(150, 48)
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


class MenuWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(25)

        title = QLabel("Welcome to Chat")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #4B0082; background: transparent;")
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(title)

        subtitle = QLabel("Connect with friends and family")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet(
            "color: #6A5ACD; background: transparent; margin-bottom: 15px;")
        subtitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(subtitle)

        signup_colors = {
            "normal_top": QColor("#7B68EE"),
            "normal_bottom": QColor("#6A5ACD"),
            "hover_top": QColor("#9370DB"),
            "hover_bottom": QColor("#7B68EE"),
            "text": "#FFFFFF"
        }

        login_colors = {
            "normal_top": QColor("#FF69B4"),
            "normal_bottom": QColor("#FF1493"),
            "hover_top": QColor("#FFB6C1"),
            "hover_bottom": QColor("#FF69B4"),
            "text": "#FFFFFF"
        }

        signupButton = RoundedButton("Create Account", signup_colors, self)
        signupButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        signupButton.clicked.connect(self.parent.show_signup)
        layout.addWidget(signupButton, alignment=Qt.AlignCenter)

        loginButton = RoundedButton("Sign In", login_colors, self)
        loginButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        loginButton.clicked.connect(self.parent.show_login)
        layout.addWidget(loginButton, alignment=Qt.AlignCenter)

        decoration = QLabel("• • •")
        decoration.setAlignment(Qt.AlignCenter)
        decoration.setFont(QFont("Segoe UI", 16))
        decoration.setStyleSheet(
            "color: #B19CD9; background: transparent; margin-top: 10px;")
        layout.addWidget(decoration)

        layout.addStretch()

        self.setLayout(layout)
