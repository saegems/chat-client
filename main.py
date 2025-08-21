import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from views.menu import MenuWindow
from views.signup import SignupWindow
from views.login import LoginWindow
from views.home import HomeWindow
from views.new_chat import NewChatWindow
from views.chat_list import ChatList


class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(2, 2, self.width()-4, self.height()-4, 8, 8)

        if self.isEnabled():
            if self.underMouse():
                # Darker purple on hover
                painter.fillPath(path, QColor("#5E4B8B"))
            else:
                painter.fillPath(path, QColor("#6B5B95"))  # Medium purple
        else:
            painter.fillPath(path, QColor("#D3D3D3"))  # Gray when disabled

        painter.setPen(Qt.white)
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = ""

        self.setWindowTitle("Chat")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove default title bar
        # Enable translucent background
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set minimum and default window size
        self.setMinimumSize(320, 480)
        self.resize(320, 520)

        # Create central widget with rounded corners
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.central_widget.setStyleSheet("""
            #CentralWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #E6E6FA, stop: 1 #D8BFD8);
                border-radius: 16px;
                border: 1px solid #B19CD9;
            }
        """)
        self.setCentralWidget(self.central_widget)

        # Initialize window history with MenuWindow
        self.window_history = []

        # Create main vertical layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Create custom title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background: transparent;")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(8)

        # Back button
        self.back_button = RoundedButton("←")
        self.back_button.setFixedSize(32, 32)
        self.back_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        title_bar_layout.addWidget(self.back_button)

        # Title label with subtle shadow effect
        title_label = QLabel("Chat")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #4B0082;
                font-weight: bold;
                font-size: 18px;
                background: transparent;
                padding: 4px;
            }
        """)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        # Stretch factor 1 to center
        title_bar_layout.addWidget(title_label, 1)

        # Close button
        self.close_button = RoundedButton("✕")
        self.close_button.setFixedSize(32, 32)
        self.close_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.close_button.clicked.connect(self.close)
        title_bar_layout.addWidget(self.close_button)

        main_layout.addWidget(title_bar)

        # Create and add the stacked widget with subtle frame
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background: rgba(255, 255, 255, 0.7);
                border-radius: 12px;
                border: 1px solid rgba(177, 156, 217, 0.5);
            }
        """)

        # Initialize windows
        self.menu_window = MenuWindow(self)
        self.signup_window = SignupWindow(self)
        self.login_window = LoginWindow(self)
        self.home_window = HomeWindow(self)
        self.new_chat_window = NewChatWindow(self)
        self.existing_chats_window = ChatList(self)

        # Add windows to stacked widget
        self.stacked_widget.addWidget(self.menu_window)
        self.stacked_widget.addWidget(self.signup_window)
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.home_window)
        self.stacked_widget.addWidget(self.new_chat_window)
        self.stacked_widget.addWidget(self.existing_chats_window)

        # Set initial window
        self.stacked_widget.setCurrentWidget(self.menu_window)
        self.window_history.append(self.menu_window)
        self.stacked_widget.currentChanged.connect(self.update_history)

        main_layout.addWidget(self.stacked_widget)

        # Variables for window dragging
        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def show_signup(self):
        if self.stacked_widget.currentWidget() != self.signup_window:
            self.animate_transition(self.signup_window)
            self.window_history.append(self.signup_window)
            self.back_button.setEnabled(True)

    def show_login(self):
        if self.stacked_widget.currentWidget() != self.login_window:
            self.animate_transition(self.login_window)
            self.window_history.append(self.login_window)
            self.back_button.setEnabled(True)

    def show_home(self):
        if self.stacked_widget.currentWidget() != self.home_window:
            self.animate_transition(self.home_window)
            self.window_history.append(self.home_window)
            self.back_button.setEnabled(False)

    def show_new_chat(self):
        if self.stacked_widget.currentWidget() != self.new_chat_window:
            self.animate_transition(self.new_chat_window)
            self.window_history.append(self.new_chat_window)
            self.back_button.setEnabled(True)

    def show_existing_chats_list(self):
        if self.stacked_widget.currentWidget() != self.existing_chats_window:
            self.animate_transition(self.existing_chats_window)
            self.window_history.append(self.existing_chats_window)
            self.back_button.setEnabled(True)

    def animate_transition(self, new_window):
        # Create slide animation for smoother transitions
        current_index = self.stacked_widget.currentIndex()
        new_index = self.stacked_widget.indexOf(new_window)

        # Determine animation direction
        direction = "left" if new_index > current_index else "right"

        # Set the new widget
        self.stacked_widget.setCurrentWidget(new_window)

        # Simple fade effect (could be enhanced with proper animation)
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background: rgba(255, 255, 255, 0.7);
                border-radius: 12px;
                border: 1px solid rgba(177, 156, 217, 0.5);
            }
        """)

    def go_back(self):
        if len(self.window_history) > 1:
            self.window_history.pop()
            previous_window = self.window_history[-1]
            self.animate_transition(previous_window)
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
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
