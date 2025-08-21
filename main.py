import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt
from views.menu import MenuWindow
from views.signup import SignupWindow
from views.login import LoginWindow
from views.home import HomeWindow
from views.new_chat import NewChatWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat")

        # Set minimum and default window size
        self.setMinimumSize(300, 400)
        self.resize(300, 400)

        # Set gradient background
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#E6E6FA"))  # Lavender top
        gradient.setColorAt(1, QColor("#D8BFD8"))  # Mauve bottom
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # Initialize window history with MenuWindow
        self.window_history = []

        # Create a central widget and main vertical layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Create a horizontal layout for the top row
        top_layout = QHBoxLayout()

        # Set consistent font with fallback
        default_font = QFont("Segoe UI, Arial", 10)

        # Create and add the Back button
        self.back_button = QPushButton("←")
        self.back_button.setMinimumSize(30, 30)
        self.back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.back_button.setFont(QFont("Segoe UI, Arial", 12, QFont.Bold))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5; /* White */
                color: #4B0082; /* Dark purple */
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #E0E0E0; /* Light gray */
            }
            QPushButton:disabled {
                background-color: #D3D3D3; /* Gray */
                color: #888888;
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Create and add the chat label
        label = QLabel("Chat")
        label.setFont(QFont("Segoe UI, Arial", 14, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF;")  # White
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_layout.addWidget(label, alignment=Qt.AlignCenter)

        # Create and add the close button
        close_button = QPushButton("✕")
        close_button.setMinimumSize(30, 30)
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        close_button.setFont(QFont("Segoe UI, Arial", 12, QFont.Bold))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #D8BFD8; /* Mauve */
                color: #4B0082; /* Dark purple */
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #C7A4C7; /* Lighter mauve */
            }
        """)
        close_button.clicked.connect(self.close)
        top_layout.addWidget(close_button, alignment=Qt.AlignRight)

        main_layout.addLayout(top_layout)

        # Create and add the stacked widget
        self.stacked_widget = QStackedWidget()
        self.menu_window = MenuWindow(self)
        self.signup_window = SignupWindow(self)
        self.login_window = LoginWindow(self)
        self.home_window = HomeWindow(self)
        self.new_chat_window = NewChatWindow(self)

        self.stacked_widget.addWidget(self.menu_window)
        self.stacked_widget.addWidget(self.signup_window)
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.home_window)
        self.stacked_widget.addWidget(self.new_chat_window)

        self.stacked_widget.setCurrentWidget(self.menu_window)
        self.stacked_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.window_history.append(self.menu_window)
        self.stacked_widget.currentChanged.connect(self.update_history)
        main_layout.addWidget(self.stacked_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def show_signup(self):
        if self.stacked_widget.currentWidget() != self.signup_window:
            self.window_history.append(self.signup_window)
            self.stacked_widget.setCurrentWidget(self.signup_window)
            self.back_button.setEnabled(True)

    def show_login(self):
        if self.stacked_widget.currentWidget() != self.login_window:
            self.window_history.append(self.login_window)
            self.stacked_widget.setCurrentWidget(self.login_window)
            self.back_button.setEnabled(True)

    def show_home(self):
        if self.stacked_widget.currentWidget() != self.home_window:
            self.window_history.append(self.home_window)
            self.stacked_widget.setCurrentWidget(self.home_window)
            self.back_button.setEnabled(False)

    def show_new_chat(self):
        if self.stacked_widget.currentWidget() != self.new_chat_window:
            self.window_history.append(self.new_chat_window)
            self.stacked_widget.setCurrentWidget(self.new_chat_window)
            self.back_button.setEnabled(True)

    def go_back(self):
        if len(self.window_history) > 1:
            self.window_history.pop()
            previous_window = self.window_history[-1]
            self.stacked_widget.setCurrentWidget(previous_window)
            self.back_button.setEnabled(len(self.window_history) > 1)

    def update_history(self):
        current_widget = self.stacked_widget.currentWidget()
        if not self.window_history or self.window_history[-1] != current_widget:
            self.window_history.append(current_widget)
        self.back_button.setEnabled(len(self.window_history) > 1)


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
