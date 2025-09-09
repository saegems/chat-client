from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QSizePolicy, QApplication, QScrollArea
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPalette
from PyQt5.QtCore import Qt
import requests
import json
from components.chat_list_item import ChatListItem
from views.chat import ChatWindow
from config.config import SERVER


class ChatList(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.chats_fetched = False
        self.open_chat_windows = {}

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0, QColor("#F8F6FF"))
        gradient.setColorAt(1, QColor("#E6E6FA"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        title_label = QLabel("Your Conversations")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #4B0082;
            background: transparent;
            padding: 10px;
            margin-bottom: 5px;
        """)
        self.main_layout.addWidget(title_label)

        self.chats_error = QLabel("")
        self.chats_error.setFont(QFont("Segoe UI", 10))
        self.chats_error.setStyleSheet("""
            color: #FF4500;
            background: transparent;
            padding: 8px;
            border-radius: 6px;
            background-color: rgba(255, 69, 0, 0.1);
        """)
        self.chats_error.setAlignment(Qt.AlignCenter)
        self.chats_error.setWordWrap(True)
        self.chats_error.hide()  # Initially hidden
        self.main_layout.addWidget(self.chats_error)

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

        self.chats_container = QWidget()
        self.chats_layout = QVBoxLayout(self.chats_container)
        self.chats_layout.setContentsMargins(5, 5, 5, 5)
        self.chats_layout.setSpacing(12)
        self.chats_layout.addStretch()

        self.scroll_area.setWidget(self.chats_container)
        self.main_layout.addWidget(self.scroll_area)

        self.loading_label = QLabel("Loading conversations...")
        self.loading_label.setFont(QFont("Segoe UI", 11))
        self.loading_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.hide()
        self.main_layout.addWidget(self.loading_label)

        self.setLayout(self.main_layout)

    def showEvent(self, event):
        """Run get_chats when the widget is shown, reset flag when hidden."""
        if not self.chats_fetched:
            self.get_chats()
            self.chats_fetched = True
        super().showEvent(event)

    def hideEvent(self, event):
        """Reset chats_fetched when widget is hidden to refresh on next show."""
        self.chats_fetched = False
        super().hideEvent(event)

    def get_chats(self):
        """Fetch and display chats for the logged-in user."""
        username = self.parent.get_username()
        if not username:
            self.show_error("No user logged in")
            return

        for i in reversed(range(self.chats_layout.count())):
            item = self.chats_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        self.loading_label.show()
        self.chats_error.hide()

        try:
            uri = f"{SERVER}/api/chats"
            params = {"username": username}
            response = requests.get(uri, params=params, timeout=10000)
            response.raise_for_status()

            response_data = {}
            if response.content:
                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
                    self.show_error("Invalid response from server")
                    return
            else:
                print("No body received")
                self.show_error("No chats received")
                return

            if response.status_code == 200:
                self.chats_error.hide()
                chats = response_data.get("chats", [])
                if not chats:
                    self.show_info(
                        "No conversations yet. Start a new chat to begin!")
                    return

                for chat in chats:
                    display_username = (
                        chat.get("receiver", {}).get("username", "Unknown")
                        if chat.get("sender", {}).get("username") == username
                        else chat.get("sender", {}).get("username", "Unknown")
                    )
                    chat_item = ChatListItem(
                        username=display_username,
                        message=chat.get("text", ""),
                        time=chat.get("time", ""),
                        current_username=username,
                        parent=self
                    )
                    chat_item.clicked.connect(self.open_chat)
                    self.chats_layout.insertWidget(
                        self.chats_layout.count() - 1, chat_item)

            else:
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.show_error(error.get("username", ""))
                else:
                    self.show_error(error)

        except requests.exceptions.RequestException as e:
            self.show_error(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            self.show_error("Invalid response from server")
        finally:
            self.loading_label.hide()

    def open_chat(self, chat_username, current_username):
        """Open a chat window for the selected conversation"""
        if chat_username in self.open_chat_windows:
            self.open_chat_windows[chat_username].raise_()
            self.open_chat_windows[chat_username].activateWindow()
            return

        chat_window = ChatWindow(self, chat_username, current_username)
        chat_window.setWindowTitle(f"Chat with {chat_username}")
        chat_window.setWindowFlags(Qt.Window)

        chat_window.destroyed.connect(
            lambda: self.open_chat_windows.pop(chat_username, None)
        )

        self.open_chat_windows[chat_username] = chat_window

        chat_window.show()

    def show_error(self, message):
        """Display error message with appropriate styling"""
        self.chats_error.setText(message)
        self.chats_error.setStyleSheet("""
            color: #FF4500;
            background: transparent;
            padding: 8px;
            border-radius: 6px;
            background-color: rgba(255, 69, 0, 0.1);
        """)
        self.chats_error.show()

    def show_info(self, message):
        """Display informational message with different styling"""
        self.chats_error.setText(message)
        self.chats_error.setStyleSheet("""
            color: #2E8B57;
            background: transparent;
            padding: 8px;
            border-radius: 6px;
            background-color: rgba(46, 139, 87, 0.1);
        """)
        self.chats_error.show()
