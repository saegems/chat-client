from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QSizePolicy, QApplication)
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPalette
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG, QTimer
import threading
import json
import requests
import time
from components.message import MessageWidget
from utils.websocket_client import PersistentWebSocketClient
from utils.format import formatDate
from config.config import SERVER


class RoundedLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setMinimumHeight(44)
        self.setFont(QFont("Segoe UI", 11))
        self.setPlaceholderText(placeholder)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 12, 12)

        if self.hasFocus():
            painter.setPen(QColor("#7B68EE"))
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


class ChatWindow(QWidget):
    def __init__(self, parent, chat_username, current_username):
        super().__init__()
        self.parent = parent
        self.chat_username = chat_username
        self.current_username = current_username
        self.running = True
        self.is_sending = False
        self.last_message_time = None
        self.pending_messages = {}

        self.websocket_client = PersistentWebSocketClient(current_username)
        self.websocket_client.message_received.connect(
            self.handle_websocket_message)
        self.websocket_client.connection_status_changed.connect(
            self.update_connection_status)
        self.websocket_client.error_occurred.connect(
            self.handle_websocket_error)

        self.setWindowTitle(f"{chat_username}")
        self.setWindowFlags(Qt.Window)

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0, QColor("#F8F6FF"))
        gradient.setColorAt(1, QColor("#E6E6FA"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        self.setMinimumSize(800, 1000)
        self.resize(800, 1000)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #7B68EE, stop: 1 #6A5ACD);
            border-bottom: 1px solid #5C4AA8;
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        back_button = GradientButton("←", {
            "normal_top": QColor("#9370DB"),
            "normal_bottom": QColor("#7B68EE"),
            "hover_top": QColor("#A891D6"),
            "hover_bottom": QColor("#9370DB"),
            "text": "#FFFFFF"
        })
        back_button.setFixedSize(40, 40)
        back_button.clicked.connect(self.close_chat)
        header_layout.addWidget(back_button)

        chat_title = QLabel(f"{chat_username}")
        chat_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        chat_title.setStyleSheet("color: #FFFFFF; background: transparent;")
        chat_title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(chat_title, 1)

        self.connection_status = QLabel("●")
        self.connection_status.setFont(QFont("Segoe UI", 16))
        self.connection_status.setStyleSheet(
            "color: #4ECDC4; background: transparent;")
        self.connection_status.setToolTip("Ready")
        header_layout.addWidget(self.connection_status)

        main_layout.addWidget(header)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(177, 156, 217, 0.3);
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(107, 91, 149, 0.5);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(107, 91, 149, 0.7);
            }
        """)

        self.messages_container = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setContentsMargins(15, 15, 15, 15)
        self.messages_layout.setSpacing(10)
        self.messages_layout.addStretch()

        self.scroll_area.setWidget(self.messages_container)
        main_layout.addWidget(self.scroll_area)

        input_container = QWidget()
        input_container.setFixedHeight(70)
        input_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.8);
            border-top: 1px solid rgba(177, 156, 217, 0.3);
        """)

        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(15, 10, 15, 10)
        input_layout.setSpacing(10)

        self.message_input = RoundedLineEdit("Type your message...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)

        send_button_colors = {
            "normal_top": QColor("#FF69B4"),
            "normal_bottom": QColor("#FF1493"),
            "hover_top": QColor("#FFB6C1"),
            "hover_bottom": QColor("#FF69B4"),
            "text": "#FFFFFF"
        }

        self.send_button = GradientButton("Send", send_button_colors)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addWidget(input_container)

        self.setLayout(main_layout)
        self.load_previous_chats()
        self.connect_websocket()

    def load_previous_chats(self):
        """Load the previous chats between the two users"""
        try:
            uri = f"{SERVER}/api/chats/messages"
            params = {"senderUsername": self.current_username,
                      "receiverUsername": self.chat_username}
            response = requests.get(uri, params=params, timeout=10000)
            response.raise_for_status()

            response_data = {}
            if response.content:
                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
                    self.add_message(
                        "System", "Invalid response from server", "Now", False)
                    return
            else:
                print("No body received")
                self.add_message(
                    "System", "No messages received from server", "Now", False)
                return

            if response.status_code == 200:
                messages = response_data.get("messages", [])
                if not messages:
                    self.add_message(
                        "System", "No previous messages found", "Now", False)
                    return

                for message in messages:
                    sender = message.get("sender", {}).get(
                        "username", "Unknown")
                    text = message.get("text", "")
                    time_str = message.get("time", "Unknown")
                    formatted_time_str = formatDate(time_str)
                    is_own_message = (sender == self.current_username)
                    self.add_message(
                        sender, text, formatted_time_str, is_own_message)

            else:
                error = response_data.get("error", "Unknown error")
                self.add_message("System", f"Error loading messages: {
                                 error}", "Now", False)

        except requests.exceptions.RequestException as e:
            self.add_message("System", f"Network error: {
                             str(e)}", "Now", False)
        except Exception as e:
            self.add_message("System", f"Error: {str(e)}", "Now", False)
            print(str(e))

    def connect_websocket(self):
        """Connect to WebSocket server"""
        if not self.websocket_client.connect(self.chat_username):
            self.add_message(
                "System",
                "Failed to connect to chat server. Messages may not be delivered.",
                "Now",
                False
            )

    def handle_websocket_message(self, data):
        """Handle incoming WebSocket messages"""
        print(f"Handling WebSocket message: {data}")
        if data.get("status") == "welcome":
            return
        if data.get("status") == "delivered":
            sender = data.get("sender", "")
            receiver = data.get("receiver", "")
            message = data.get("message", "")
            time_str = data.get("time", "Now")
            formatted_time_str = formatDate(time_str)

            if (sender == self.current_username and
                receiver == self.chat_username and
                    message in self.pending_messages):

                message_widget = self.pending_messages[message]
                if hasattr(message_widget, 'time_label'):
                    message_widget.time_label.setText(time_str)

                del self.pending_messages[message]
                self.connection_status.setStyleSheet(
                    "color: #4ECDC4; background: transparent;")
                self.connection_status.setToolTip("Message delivered")

        elif (data.get("sender") == self.chat_username and
              data.get("receiver") == self.current_username and
              data.get("status") != "delivered"):
            sender = data.get("sender", "")
            message = data.get("message", "")
            time_str = data.get("time", "Now")
            formatted_time_str = formatDate(time_str)

            print(f"Adding incoming message from {sender}: {message}")
            self.add_message(sender, message, formatted_time_str, False)

    def update_connection_status(self, status, tooltip):
        """Update the connection status indicator"""
        color_map = {
            "connected": "#4ECDC4",
            "connecting": "#FFD93D",
            "disconnected": "#FF6B6B"
        }

        color = color_map.get(status, "#FF6B6B")
        self.connection_status.setStyleSheet(
            f"color: {color}; background: transparent;")
        self.connection_status.setToolTip(tooltip)

    def handle_websocket_error(self, error_message):
        """Handle WebSocket errors"""
        self.add_message("System", f"Connection error: {
                         error_message}", "Now", False)
        self.connection_status.setStyleSheet(
            "color: #FF6B6B; background: transparent;")
        self.connection_status.setToolTip(f"Error: {error_message}")

    def add_message(self, username, message, time, is_own_message):
        """Add a message to the chat"""
        message_widget = MessageWidget(
            username, message, time, is_own_message, self)
        self.messages_layout.insertWidget(
            self.messages_layout.count() - 1, message_widget)

        if is_own_message and username == "You":
            self.pending_messages[message] = message_widget

        QApplication.processEvents()
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def send_message(self):
        """Send a message through the persistent WebSocket connection"""
        message = self.message_input.text().strip()
        if not message or self.is_sending:
            return

        self.add_message("You", message, "Delivered", True)
        self.message_input.clear()

        self.connection_status.setStyleSheet(
            "color: #FFD93D; background: transparent;")
        self.connection_status.setToolTip("Sending message...")
        self.is_sending = True

        if self.websocket_client.send_message(self.chat_username, message):
            self.is_sending = False
        else:
            self.is_sending = False
            self.add_message("System", "Failed to send message", "Now", False)
            self.connection_status.setStyleSheet(
                "color: #FF6B6B; background: transparent;")
            self.connection_status.setToolTip("Failed to send message")

    def close_chat(self):
        """Close chat window and WebSocket connection"""
        self.running = False
        if hasattr(self, 'websocket_client'):
            self.websocket_client.close()
        self.close()
        self.deleteLater()

    def closeEvent(self, event):
        """Handle window close event"""
        self.close_chat()
        event.accept()
