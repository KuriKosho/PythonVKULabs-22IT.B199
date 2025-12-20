from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from SubscriptionManagerApp.app.controllers.auth_controller import AuthController
from PyQt6.QtGui import QPixmap

from SubscriptionManagerApp.app.utils.section import Session


class LoginWindow(QWidget):
    loginSuccess = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login | Subscription Manager")
        self.setFixedSize(420, 560)

        root_layout = QVBoxLayout(self)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Card =====
        self.card = QFrame()
        self.card.setObjectName("LoginCard")

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== LOGO =====
        logo_label = QLabel()
        logo_label.setObjectName("AppLogo")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Đổi đường dẫn logo tại đây
        pixmap = QPixmap("SubscriptionManagerApp/assets/icons/logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(
                pixmap.scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
            )
        else:
            logo_label.setText("🧩")

        app_name = QLabel("Subscription Manager")
        app_name.setObjectName("AppName")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Title =====
        title = QLabel("Welcome Back")
        title.setObjectName("LoginTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sign in to manage your subscriptions")
        subtitle.setObjectName("LoginSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== Inputs =====
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.user_input.setText("admin")

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setText("123456")
        self.pass_input.returnPressed.connect(self.handle_login)

        # ===== Buttons =====
        btn_login = QPushButton("Sign In")
        btn_login.setObjectName("BtnPrimary")
        btn_login.clicked.connect(self.handle_login)

        btn_register = QPushButton("Create Account")
        btn_register.setObjectName("BtnSecondary")
        btn_register.clicked.connect(self.handle_register)

        # ===== Add to layout =====
        card_layout.addWidget(logo_label)
        card_layout.addWidget(app_name)
        card_layout.addSpacing(10)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(12)
        card_layout.addWidget(self.user_input)
        card_layout.addWidget(self.pass_input)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_login)
        card_layout.addWidget(btn_register)

        root_layout.addWidget(self.card)

    # ===== Logic giữ nguyên =====
    def handle_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password.")
            return
        user = self.auth_controller.login(username, password)
        if user:
            Session.login(user)
            self.loginSuccess.emit()
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password.")

    def handle_register(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password.")
            return

        user = self.auth_controller.register(username, password)
        if user:
            QMessageBox.information(
                self, "Success",
                "Account created successfully! You can log in now."
            )
        else:
            QMessageBox.critical(
                self, "Failed",
                "Username already exists."
            )
