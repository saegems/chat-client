from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QLinearGradient, QColor, QPalette
from PyQt5.QtCore import Qt
import requests
import json
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
        self.setMinimumSize(140, 48)
        self.setFont(QFont("Segoe UI", 11, QFont.Bold))

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


class Profile(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.edit_mode = None

        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, 600)
        gradient.setColorAt(0, QColor("#F5F0FF"))  # Very light lavender
        gradient.setColorAt(1, QColor("#E6E6FA"))  # Lavender
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title_label = QLabel("Your Profile")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "color: #4B0082; background: transparent; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        profile_container = QWidget()
        profile_container.setStyleSheet("""
            background: rgba(255, 255, 255, 0.7);
            border-radius: 16px;
            border: 1px solid rgba(177, 156, 217, 0.3);
        """)
        self.profile_layout = QVBoxLayout(profile_container)
        self.profile_layout.setContentsMargins(25, 25, 25, 25)
        self.profile_layout.setSpacing(20)

        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 12, QFont.Medium))
        username_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        self.profile_layout.addWidget(username_label)

        # Initialize with placeholder, will be updated when shown
        self.username_display = QLabel("Loading...")
        self.username_display.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.username_display.setStyleSheet("""
            color: #4B0082;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 8px;
            padding: 10px;
            border: 1px solid rgba(177, 156, 217, 0.2);
        """)
        self.username_display.setAlignment(Qt.AlignCenter)
        self.profile_layout.addWidget(self.username_display)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        edit_username_colors = {
            "normal_top": QColor("#9370DB"),
            "normal_bottom": QColor("#7B68EE"),
            "hover_top": QColor("#A891D6"),
            "hover_bottom": QColor("#9370DB"),
            "text": "#FFFFFF"
        }

        self.edit_username_btn = GradientButton(
            "Edit Username", edit_username_colors, self)
        self.edit_username_btn.clicked.connect(
            lambda: self.show_edit_form("username"))
        buttons_layout.addWidget(self.edit_username_btn)

        change_password_colors = {
            "normal_top": QColor("#FF69B4"),
            "normal_bottom": QColor("#FF1493"),
            "hover_top": QColor("#FFB6C1"),
            "hover_bottom": QColor("#FF69B4"),
            "text": "#FFFFFF"
        }

        self.change_password_btn = GradientButton(
            "Change Password", change_password_colors, self)
        self.change_password_btn.clicked.connect(
            lambda: self.show_edit_form("password"))
        buttons_layout.addWidget(self.change_password_btn)

        self.profile_layout.addLayout(buttons_layout)

        # Create edit form widgets but don't add them to layout yet
        self.create_edit_forms()

        main_layout.addWidget(profile_container)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def create_edit_forms(self):
        """Create edit form widgets but don't add to layout yet"""
        # Username edit form container
        self.username_form_container = QWidget()
        username_form_layout = QVBoxLayout(self.username_form_container)
        username_form_layout.setContentsMargins(0, 0, 0, 0)
        username_form_layout.setSpacing(15)

        new_username_label = QLabel("New Username")
        new_username_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        new_username_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        username_form_layout.addWidget(new_username_label)

        self.new_username_input = RoundedLineEdit("Enter new username")
        self.new_username_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
            }
        """)
        username_form_layout.addWidget(self.new_username_input)

        self.username_error = QLabel("")
        self.username_error.setFont(QFont("Segoe UI", 9))
        self.username_error.setStyleSheet(
            "color: #FF4500; background: transparent;")
        self.username_error.setWordWrap(True)
        username_form_layout.addWidget(self.username_error)

        username_buttons_layout = QHBoxLayout()
        username_buttons_layout.setSpacing(10)

        cancel_colors = {
            "normal_top": QColor("#D8BFD8"),
            "normal_bottom": QColor("#C7A4C7"),
            "hover_top": QColor("#E6E6FA"),
            "hover_bottom": QColor("#D8BFD8"),
            "text": "#4B0082"
        }

        self.username_cancel_btn = GradientButton(
            "Cancel", cancel_colors, self)
        self.username_cancel_btn.clicked.connect(self.hide_edit_form)
        username_buttons_layout.addWidget(self.username_cancel_btn)

        save_colors = {
            "normal_top": QColor("#7B68EE"),
            "normal_bottom": QColor("#6A5ACD"),
            "hover_top": QColor("#9370DB"),
            "hover_bottom": QColor("#7B68EE"),
            "text": "#FFFFFF"
        }

        self.username_save_btn = GradientButton(
            "Save Changes", save_colors, self)
        self.username_save_btn.clicked.connect(self.save_changes)
        username_buttons_layout.addWidget(self.username_save_btn)

        username_form_layout.addLayout(username_buttons_layout)

        self.password_form_container = QWidget()
        password_form_layout = QVBoxLayout(self.password_form_container)
        password_form_layout.setContentsMargins(0, 0, 0, 0)
        password_form_layout.setSpacing(15)

        current_password_label = QLabel("Current Password")
        current_password_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        current_password_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        password_form_layout.addWidget(current_password_label)

        self.current_password_input = RoundedLineEdit("Enter current password")
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
            }
        """)
        password_form_layout.addWidget(self.current_password_input)

        new_password_label = QLabel("New Password")
        new_password_label.setFont(QFont("Segoe UI", 10, QFont.Medium))
        new_password_label.setStyleSheet(
            "color: #6A5ACD; background: transparent;")
        password_form_layout.addWidget(new_password_label)

        self.new_password_input = RoundedLineEdit("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet("""
            QLineEdit {
                background: #FFFFFF;
                color: #4B0082;
                padding: 8px 12px;
                selection-background-color: #D8BFD8;
            }
        """)
        password_form_layout.addWidget(self.new_password_input)

        self.password_error = QLabel("")
        self.password_error.setFont(QFont("Segoe UI", 9))
        self.password_error.setStyleSheet(
            "color: #FF4500; background: transparent;")
        self.password_error.setWordWrap(True)
        password_form_layout.addWidget(self.password_error)

        password_buttons_layout = QHBoxLayout()
        password_buttons_layout.setSpacing(10)

        self.password_cancel_btn = GradientButton(
            "Cancel", cancel_colors, self)
        self.password_cancel_btn.clicked.connect(self.hide_edit_form)
        password_buttons_layout.addWidget(self.password_cancel_btn)

        self.password_save_btn = GradientButton(
            "Save Changes", save_colors, self)
        self.password_save_btn.clicked.connect(self.save_changes)
        password_buttons_layout.addWidget(self.password_save_btn)

        password_form_layout.addLayout(password_buttons_layout)

    def showEvent(self, event):
        """Override showEvent to update the username when the window is shown"""
        super().showEvent(event)
        self.update_username_display()

    def update_username_display(self):
        """Update the username display with the current username"""
        username = self.parent.get_username()
        if username:
            self.username_display.setText(username)
        else:
            self.username_display.setText("Not logged in")

    def show_edit_form(self, form_type):
        """Show the appropriate edit form in the same window"""
        self.edit_mode = form_type

        self.edit_username_btn.setVisible(False)
        self.change_password_btn.setVisible(False)

        self.username_error.setText("")
        self.password_error.setText("")

        self.remove_existing_forms()

        if form_type == "username":
            self.profile_layout.addWidget(self.username_form_container)
            self.new_username_input.setText("")
            self.new_username_input.setFocus()
        else:
            self.profile_layout.addWidget(self.password_form_container)
            self.current_password_input.setText("")
            self.new_password_input.setText("")
            self.current_password_input.setFocus()

    def remove_existing_forms(self):
        """Remove any existing form widgets from layout"""
        try:
            self.profile_layout.removeWidget(self.username_form_container)
            self.username_form_container.setParent(None)
        except:
            pass

        try:
            self.profile_layout.removeWidget(self.password_form_container)
            self.password_form_container.setParent(None)
        except:
            pass

    def hide_edit_form(self):
        """Hide the edit form and show action buttons again"""
        self.edit_mode = None
        self.remove_existing_forms()
        self.edit_username_btn.setVisible(True)
        self.change_password_btn.setVisible(True)
        self.new_username_input.setText("")
        self.current_password_input.setText("")
        self.new_password_input.setText("")
        self.username_error.setText("")
        self.password_error.setText("")

    def save_changes(self):
        """Save changes based on current edit mode"""
        if self.edit_mode == "username":
            self.update_username()
        else:
            self.update_password()

    def update_username(self):
        """Update username via API"""
        new_username = self.new_username_input.text().strip()

        if not new_username:
            self.username_error.setText("Please enter a new username")
            return

        if new_username == self.parent.get_username():
            self.username_error.setText(
                "New username cannot be the same as current username")
            return

        try:
            uri = f"{SERVER}/api/users/username"
            params = {"oldUsername": self.parent.get_username(),
                      "newUsername": new_username}
            response = requests.put(uri, params=params, timeout=5)
            response.raise_for_status()
            response_data = {}

            if response.content:
                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    self.username_error.setText("Response is not valid JSON")
            else:
                self.username_error.setText("No body received")

            if response.status_code == 200:
                self.new_username_input.clear()
                self.parent.set_username(new_username)
                self.update_username_display()
                self.hide_edit_form()
            else:
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.username_error.setText(error.get("username", ""))
                else:
                    self.username_error.setText(error)

        except Exception as e:
            self.username_error.setText(str(e))

    def update_password(self):
        """Update password via API"""
        current_password = self.current_password_input.text().strip()
        new_password = self.new_password_input.text().strip()

        if not current_password:
            self.password_error.setText("Please enter your current password")
            return

        if not new_password:
            self.password_error.setText("Please enter a new password")
            return

        if current_password == new_password:
            self.password_error.setText(
                "New password cannot be the same as current password")
            return

        try:
            uri = f"{SERVER}/api/users/password"
            params = {"username": self.parent.get_username(),
                      "oldPassword": current_password,
                      "newPassword": new_password}
            response = requests.put(uri, params=params, timeout=5)
            response.raise_for_status()
            response_data = {}

            if response.content:
                try:
                    response_data = response.json()
                except json.JSONDecodeError:
                    self.password_error.setText("Response is not valid JSON")
            else:
                self.password_error.setText("No body received")

            if response.status_code == 200:
                self.hide_edit_form()
            else:
                error = response_data.get("error", "Unknown error")
                if isinstance(error, dict):
                    self.password_error.setText(error.get("username", ""))
                else:
                    self.password_error.setText(error)

        except Exception as e:
            self.password_error.setText(str(e))
