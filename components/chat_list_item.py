from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient, QMouseEvent
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from views.chat import ChatWindow


class ChatListItem(QWidget):
    clicked = pyqtSignal(str, str)

    def __init__(self, username, message, time, current_username, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)
        self.chat_username = username
        self.current_username = current_username
        self.parent_list = parent

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(8)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)

        username_label = QLabel(username)
        username_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        username_label.setStyleSheet(
            "color: #4B0082; background: transparent;")
        username_label.setAlignment(Qt.AlignLeft)
        top_layout.addWidget(username_label, 1)

        time_label = QLabel(time)
        time_label.setFont(QFont("Segoe UI", 9))
        time_label.setStyleSheet("color: #9370DB; background: transparent;")
        time_label.setAlignment(Qt.AlignRight)
        top_layout.addWidget(time_label)

        main_layout.addLayout(top_layout)

        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 10))
        message_label.setStyleSheet("color: #6A5ACD; background: transparent;")
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setWordWrap(True)
        message_label.setMaximumHeight(40)
        message_label.setTextFormat(Qt.PlainText)
        main_layout.addWidget(message_label)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #FAF0FF, stop: 1 #F5EBFF);
                border-radius: 12px;
                padding: 2px;
            }
            QWidget:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #F0E6FF, stop: 1 #EBD6FF);
                border: 1px solid #D8BFD8;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(107, 91, 149, 80))
        self.setGraphicsEffect(shadow)

        self.setMouseTracking(True)

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse click events"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.chat_username, self.current_username)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Change cursor to pointing hand on hover"""
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Revert cursor to arrow when not hovering"""
        self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)

    def paintEvent(self, event):
        """Custom paint event to draw rounded corners with gradient"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(2, 2, self.width()-4, self.height()-4, 10, 10)

        gradient = QLinearGradient(0, 0, 0, self.height())
        if self.underMouse():
            gradient.setColorAt(0, QColor(240, 230, 255))
            gradient.setColorAt(1, QColor(235, 214, 255))
        else:
            gradient.setColorAt(0, QColor(250, 240, 255))
            gradient.setColorAt(1, QColor(245, 235, 255))

        painter.fillPath(path, gradient)

        painter.setPen(QColor(177, 156, 217, 100))
        painter.drawPath(path)
