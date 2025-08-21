from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QColor, QPainter, QPainterPath, QLinearGradient
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class ChatListItem(QWidget):
    def __init__(self, username, message, time, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(80)  # Ensure consistent height

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(8)

        # Top row with username and time
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)

        # Username with prominent styling
        username_label = QLabel(username)
        username_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        username_label.setStyleSheet(
            "color: #4B0082; background: transparent;")
        username_label.setAlignment(Qt.AlignLeft)
        top_layout.addWidget(username_label, 1)  # Allow username to expand

        # Time with subtle styling
        time_label = QLabel(time)
        time_label.setFont(QFont("Segoe UI", 9))
        time_label.setStyleSheet("color: #9370DB; background: transparent;")
        time_label.setAlignment(Qt.AlignRight)
        top_layout.addWidget(time_label)

        main_layout.addLayout(top_layout)

        # Message preview with ellipsis for long text
        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 10))
        message_label.setStyleSheet("color: #6A5ACD; background: transparent;")
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setWordWrap(True)
        message_label.setMaximumHeight(40)  # Limit height with ellipsis
        message_label.setTextFormat(Qt.PlainText)
        main_layout.addWidget(message_label)

        self.setLayout(main_layout)

        # Custom styling with gradient and rounded corners
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
            }
        """)

        # Enhanced shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(107, 91, 149, 80))  # Purple tinted shadow
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        """Custom paint event to draw rounded corners with gradient"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(2, 2, self.width()-4, self.height()-4, 10, 10)

        # Create gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        if self.underMouse():
            gradient.setColorAt(0, QColor(240, 230, 255))  # Light lavender
            # Slightly darker lavender
            gradient.setColorAt(1, QColor(235, 214, 255))
        else:
            gradient.setColorAt(0, QColor(250, 240, 255)
                                )  # Very light lavender
            gradient.setColorAt(1, QColor(245, 235, 255))  # Slightly darker

        painter.fillPath(path, gradient)

        # Draw border
        painter.setPen(QColor(177, 156, 217, 100))  # Soft purple border
        painter.drawPath(path)
