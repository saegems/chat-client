from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QSizePolicy, QApplication
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPalette
from PyQt5.QtGui import QTextOption
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG
import requests
import json
import threading
from utils.websocket_client import PersistentWebSocketClient
from utils.crypt import encrypt, compress
from config.config import SERVER


class RoundedLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 44)
        self.setFont(QFont("Segoe UI", 11))
        self.setPlaceholderText(placeholder)

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


class RoundedTextEdit(QTextEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 100)
        self.setFont(QFont("Segoe UI", 11))
        self.setPlaceholderText(placeholder)

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
        self.setMinimumSize(100, 44)
        self.setFont(QFont("Segoe UI", 11, QFont.Bold))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(2, 2, self.width()-4, self.height()-4, 10, 10)

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


class NewChatWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.websocket_client = None
        self.message_sent = False

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0, QColor("#F5F0FF"))
        gradient.setColorAt(1, QColor("#E6E6FA"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        title_label = QLabel("Start a New Chat")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "color: #4B0082; background: transparent; margin-bottom: 10px;")
        self.main_layout.addWidget(title_label)

        form_container = QWidget()
        form_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px;
            border: 1px solid rgba(177, 156, 217, 0.3);
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        username_label = QLabel("Find User")
        username_label.setFont(QFont("Segoe UI", 11, QFont.Medium))
        username_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        form_layout.addWidget(username_label)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        self.username_input = RoundedLineEdit("Enter username to find")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
            }
        """)
        top_layout.addWidget(self.username_input)

        find_button_colors = {
            "normal_top": QColor("#7B68EE"),
            "normal_bottom": QColor("#6A5ACD"),
            "hover_top": QColor("#9370DB"),
            "hover_bottom": QColor("#7B68EE"),
            "text": "#FFFFFF"
        }

        find_button = GradientButton("Find", find_button_colors, self)
        find_button.clicked.connect(self.find_user)
        top_layout.addWidget(find_button)

        form_layout.addLayout(top_layout)

        self.error_message = QLabel("")
        self.error_message.setFont(QFont("Segoe UI", 10))
        self.error_message.setStyleSheet(
            "color: #FF4500; background: transparent;")
        self.error_message.setAlignment(Qt.AlignLeft)
        self.error_message.setWordWrap(True)
        form_layout.addWidget(self.error_message)

        message_label = QLabel("Your Message")
        message_label.setFont(QFont("Segoe UI", 11, QFont.Medium))
        message_label.setStyleSheet("color: #6A5ACD; background: transparent;")
        form_layout.addWidget(message_label)

        self.message_input = RoundedTextEdit("Type your message here...")
        self.message_input.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.message_input.setLineWrapMode(QTextEdit.WidgetWidth)
        self.message_input.setWordWrapMode(
            QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.message_input.setStyleSheet("""
            QTextEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
            }
        """)
        self.message_input.setDisabled(True)
        form_layout.addWidget(self.message_input)

        send_button_colors = {
            "normal_top": QColor("#FF69B4"),
            "normal_bottom": QColor("#FF1493"),
            "hover_top": QColor("#FFB6C1"),
            "hover_bottom": QColor("#FF69B4"),
            "text": "#FFFFFF"
        }

        self.send_button = GradientButton(
            "Send Message", send_button_colors, self)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setVisible(False)
        form_layout.addWidget(self.send_button, alignment=Qt.AlignRight)

        self.main_layout.addWidget(form_container)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

    def change_view(self):
        """Enable message input and show Send button."""
        self.error_message.setText("")
        self.message_input.setDisabled(False)
        self.send_button.setVisible(True)
        self.error_message.setStyleSheet(
            "color: #2E8B57; background: transparent;")
        self.error_message.setText("✓ User found! You can now send a message.")

    def find_user(self):
        """Search for a user via API and switch to chat view if found."""
        self.error_message.setText("")
        self.error_message.setStyleSheet(
            "color: #FF4500; background: transparent;")
        username = self.username_input.text().strip()
        if not username:
            self.error_message.setText("Please enter a username")
            self.message_input.setDisabled(True)
            self.send_button.setVisible(False)
            return

        try:
            uri = f"{SERVER}/api/users"
            encrypted_username = encrypt(username)
            compressed_username = compress(encrypted_username)
            params = {"username": compressed_username}
            response = requests.get(uri, params=params, timeout=10000)
            response.raise_for_status()

            try:
                response_data = response.json()
            except json.JSONDecodeError:
                self.error_message.setText("Invalid response from server")
                self.message_input.setDisabled(True)
                self.send_button.setVisible(False)
                return

            if response.status_code == 200:
                self.change_view()
            else:
                self.message_input.setDisabled(True)
                self.send_button.setVisible(False)
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.error_message.setText(error.get("username", ""))
                else:
                    self.error_message.setText(error)

        except requests.exceptions.RequestException as e:
            self.error_message.setText(f"Network error: {str(e)}")
            self.message_input.setDisabled(True)
            self.send_button.setVisible(False)

    def handle_websocket_message(self, data):
        """Handle incoming WebSocket messages."""
        print(f"Received WebSocket message: {data}")
        if data.get("status") == "welcome":
            return
        if data.get("status") == "delivered":
            self.message_sent = True
            QMetaObject.invokeMethod(
                self.message_input, "clear", Qt.QueuedConnection
            )
            QMetaObject.invokeMethod(
                self.error_message,
                "setText",
                Qt.QueuedConnection,
                Q_ARG(str, "✓ Message sent successfully!")
            )
            QMetaObject.invokeMethod(
                self.error_message,
                "setStyleSheet",
                Qt.QueuedConnection,
                Q_ARG(str, "color: #2E8B57; background: transparent;")
            )
            if self.websocket_client:
                self.websocket_client.close()
                self.websocket_client = None

    def handle_websocket_error(self, error_message):
        """Handle WebSocket errors."""
        QMetaObject.invokeMethod(
            self.error_message,
            "setText",
            Qt.QueuedConnection,
            Q_ARG(str, f"WebSocket error: {error_message}")
        )
        QMetaObject.invokeMethod(
            self.error_message,
            "setStyleSheet",
            Qt.QueuedConnection,
            Q_ARG(str, "color: #FF4500; background: transparent;")
        )

        if self.websocket_client:
            self.websocket_client.close()
            self.websocket_client = None

    def update_connection_status(self, status, tooltip):
        """Update the connection status indicator."""
        pass

    def send_message(self):
        """Send a message using the persistent WebSocket client."""
        self.error_message.setText("")
        self.error_message.setStyleSheet(
            "color: #FF4500; background: transparent;")

        message = self.message_input.toPlainText().strip()
        sender = self.parent.get_username()
        receiver = self.username_input.text().strip()

        if not message:
            self.error_message.setText("Please enter a message")
            return

        if not sender:
            self.error_message.setText("No user logged in")
            return

        if not self.websocket_client:
            encrypted_sender = encrypt(sender)
            compressed_sender = compress(encrypted_sender)
            self.websocket_client = PersistentWebSocketClient(
                compressed_sender)
            self.websocket_client.message_received.connect(
                self.handle_websocket_message)
            self.websocket_client.error_occurred.connect(
                self.handle_websocket_error)

            encrypted_receiver = encrypt(receiver)
            compressed_receiver = compress(encrypted_receiver)
            if not self.websocket_client.connect(compressed_receiver):
                self.error_message.setText("Failed to connect to chat server")
                return

        encrypted_message = encrypt(message)
        compressed_message = compress(encrypted_message)
        encrypted_receiver = encrypt(receiver)
        compressed_receiver = compress(encrypted_receiver)
        if self.websocket_client.send_message(compressed_receiver, compressed_message):
            self.error_message.setText("Sending message...")
            self.error_message.setStyleSheet(
                "color: #FFD93D; background: transparent;")
        else:
            self.error_message.setText("Failed to send message")
            self.error_message.setStyleSheet(
                "color: #FF4500; background: transparent;")

            if self.websocket_client:
                self.websocket_client.close()
                self.websocket_client = None

    def closeEvent(self, event):
        """Clean up WebSocket connection when window is closed."""
        if self.websocket_client:
            self.websocket_client.close()
        event.accept()
