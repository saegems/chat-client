import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor
from PyQt5.QtCore import Qt
from menu import MenuWindow
from signup import SignupWindow
from login import LoginWindow
from home import HomeWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat")

        # Enable high-DPI scaling for Windows compatibility

        # Set minimum and default window size instead of fixed size
        self.setMinimumSize(300, 400)  # Minimum size for usability
        self.resize(300, 400)  # Default size, allows resizing

        # Set gradient background
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0, QColor("#1e1e2e"))  # Dark top
        gradient.setColorAt(1, QColor("#3b3b4f"))  # Lighter bottom
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # Initialize window history with MenuWindow
        self.window_history = []

        # Create a central widget and main vertical layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        # Reduced margins for better scaling
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)  # Adjusted spacing for consistency

        # Create a horizontal layout for the top row
        top_layout = QHBoxLayout()

        # Set consistent font with fallback
        default_font = QFont("Segoe UI", 10)  # Base font size for scalability
        # Fallback to Arial if Segoe UI unavailable
        default_font.setFamily("Segoe UI, Arial")

        # Create and add the Back button with left arrow icon
        self.back_button = QPushButton("←")  # Unicode left arrow
        # Minimum size instead of fixed
        self.back_button.setMinimumSize(30, 30)
        self.back_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.back_button.setFont(
            QFont("Segoe UI, Arial", 12, QFont.Bold))  # Smaller, bold font
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #b2beb5;
                color: white;
                border-radius: 4px; /* Slightly larger for high-DPI */
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #a9a9a9;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
        """)
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)  # Disabled initially
        top_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Create and add the chat label to the top-center
        label = QLabel("Chat")
        # Smaller font for scaling
        label.setFont(QFont("Segoe UI, Arial", 14, QFont.Bold))
        label.setStyleSheet("color: #e0e0e0;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        top_layout.addWidget(label, alignment=Qt.AlignCenter)

        # Create and add the close button with 'X' icon to the top-right
        close_button = QPushButton("✕")  # Unicode 'X' character
        close_button.setMinimumSize(30, 30)  # Minimum size instead of fixed
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Smaller, bold font
        close_button.setFont(QFont("Segoe UI, Arial", 12, QFont.Bold))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: white;
                border-radius: 4px; /* Slightly larger for high-DPI */
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #ff7777;
            }
        """)
        close_button.clicked.connect(self.close)
        top_layout.addWidget(close_button, alignment=Qt.AlignRight)

        # Add the top layout to the main layout
        main_layout.addLayout(top_layout)

        # Create and add the stacked widget
        self.stacked_widget = QStackedWidget()
        self.menu_window = MenuWindow(self)
        self.signup_window = SignupWindow(self)
        self.login_window = LoginWindow(self)
        self.home_window = HomeWindow(self)

        self.stacked_widget.addWidget(self.menu_window)
        self.stacked_widget.addWidget(self.signup_window)
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.home_window)
        self.stacked_widget.setCurrentWidget(self.menu_window)
        self.stacked_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.window_history.append(self.menu_window)  # Initialize history
        self.stacked_widget.currentChanged.connect(self.update_history)
        main_layout.addWidget(self.stacked_widget)

        # Set the layout to the central widget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_signup(self):
        """Switch to the SignupWindow and update history."""
        if self.stacked_widget.currentWidget() != self.signup_window:
            self.window_history.append(self.signup_window)
            self.stacked_widget.setCurrentWidget(self.signup_window)
            self.back_button.setEnabled(True)

    def show_login(self):
        """Switch to the LoginWindow and update history."""
        if self.stacked_widget.currentWidget() != self.login_window:
            self.window_history.append(self.login_window)
            self.stacked_widget.setCurrentWidget(self.login_window)
            self.back_button.setEnabled(True)

    def show_home(self):
        """Switch to the HomeWindow and update history."""
        if self.stacked_widget.currentWidget() != self.home_window:
            self.window_history.append(self.home_window)
            self.stacked_widget.setCurrentWidget(self.home_window)
            self.back_button.setEnabled(False)

    def go_back(self):
        """Switch to the previous window in the history."""
        if len(self.window_history) > 1:  # Ensure there's a previous window
            self.window_history.pop()  # Remove current window
            previous_window = self.window_history[-1]  # Get previous window
            self.stacked_widget.setCurrentWidget(previous_window)
            self.back_button.setEnabled(len(self.window_history) > 1)

    def update_history(self):
        """Update the window history when the current widget changes."""
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
