from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QColor, QLinearGradient
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class MessageBubble(QWidget):
    def __init__(self, username, message, time, is_own_message=False, parent=None):
        super().__init__(parent)
        self.is_own_message = is_own_message
        self.setMinimumHeight(60)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(4)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(8)

        username_label = QLabel(username)
        username_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        username_label.setStyleSheet(
            "color: #4B0082; background: transparent;")
        username_label.setAlignment(Qt.AlignLeft)
        top_layout.addWidget(username_label, 1)

        time_label = QLabel(time)
        time_label.setFont(QFont("Segoe UI", 9))
        time_label.setStyleSheet("color: #6A5ACD; background: transparent;")
        time_label.setAlignment(Qt.AlignRight)
        top_layout.addWidget(time_label)

        main_layout.addLayout(top_layout)

        message_label = QLabel(message)
        message_label.setFont(QFont("Segoe UI", 11))
        message_label.setStyleSheet("color: #4B0082; background: transparent;")
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setWordWrap(True)
        message_label.setTextFormat(Qt.PlainText)
        main_layout.addWidget(message_label)

        self.setLayout(main_layout)

        if self.is_own_message:
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #E6E6FA, stop: 1 #D8BFD8);
                    border-radius: 12px;
                    padding: 2px;
                    margin-left: 40px;
                    margin-right: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #FFFFFF, stop: 1 #F5F0FF);
                    border-radius: 12px;
                    padding: 2px;
                    margin-left: 10px;
                    margin-right: 40px;
                }
            """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(107, 91, 149, 60))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        """Custom paint event to draw rounded corners with gradient"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(2, 2, self.width()-4, self.height()-4, 10, 10)

        gradient = QLinearGradient(0, 0, 0, self.height())

        if self.is_own_message:
            gradient.setColorAt(0, QColor(230, 230, 250))
            gradient.setColorAt(1, QColor(216, 191, 216))
        else:
            gradient.setColorAt(0, QColor(255, 255, 255))
            gradient.setColorAt(1, QColor(245, 240, 255))

        painter.fillPath(path, gradient)

        if self.is_own_message:
            painter.setPen(QColor(177, 156, 217, 120))
        else:
            painter.setPen(QColor(200, 200, 220, 100))
        painter.drawPath(path)


class MessageWidget(QWidget):
    def __init__(self, username, message, time, is_own_message=False, parent=None):
        super().__init__(parent)
        self.is_own_message = is_own_message

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)

        if self.is_own_message:
            main_layout.addStretch()

        self.message_bubble = MessageBubble(
            username, message, time, is_own_message, self)
        main_layout.addWidget(self.message_bubble)

        if not self.is_own_message:
            main_layout.addStretch()

        self.setLayout(main_layout)
