from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QFormLayout,
    QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt

from SubscriptionManagerApp.app.controllers.auth_controller import AuthController
from SubscriptionManagerApp.app.config import APP_NAME
from SubscriptionManagerApp.app.data.settings_dao import SettingsDAO
from SubscriptionManagerApp.app.utils.section import Session


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.settings_dao = SettingsDAO()
        self.current_user = Session.get_user()

        self.init_ui()
        self.load_current_settings()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)
        self.layout.setSpacing(20)

        # ================= HEADER =================
        lbl_title = QLabel("CÀI ĐẶT HỆ THỐNG")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        self.layout.addWidget(lbl_title)

        # ================= APP INFO =================
        group_info = QGroupBox("Thông tin ứng dụng")
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel(f"Tên phần mềm: {APP_NAME}"))
        info_layout.addWidget(QLabel("Phiên bản: 1.1.0"))
        group_info.setLayout(info_layout)
        self.layout.addWidget(group_info)

        # ================= EMAIL SETTINGS =================
        group_email = QGroupBox("Cấu hình Email Gửi Thông Báo (Gmail)")
        email_layout = QFormLayout()

        self.inp_smtp_email = QLineEdit()
        self.inp_smtp_email.setPlaceholderText("myapp@gmail.com")

        self.inp_smtp_pass = QLineEdit()
        self.inp_smtp_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.inp_smtp_pass.setPlaceholderText("App Password")

        btn_save_email = QPushButton("Lưu Cấu Hình Email")
        btn_save_email.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save_email.setStyleSheet("background-color:#3498db;color:white;padding:8px;")
        btn_save_email.clicked.connect(self.handle_save_email_config)

        email_layout.addRow("Email gửi:", self.inp_smtp_email)
        email_layout.addRow("Mật khẩu ứng dụng:", self.inp_smtp_pass)
        email_layout.addRow("", btn_save_email)

        group_email.setLayout(email_layout)
        self.layout.addWidget(group_email)

        # ================= CHANGE PASSWORD =================
        group_auth = QGroupBox("Đổi Mật Khẩu")
        form_layout = QFormLayout()

        self.inp_username = QLineEdit()
        self.inp_username.setReadOnly(True)
        self.inp_username.setText(self.current_user["username"])

        self.inp_old_pass = QLineEdit()
        self.inp_old_pass.setEchoMode(QLineEdit.EchoMode.Password)

        self.inp_new_pass = QLineEdit()
        self.inp_new_pass.setEchoMode(QLineEdit.EchoMode.Password)

        self.inp_confirm_pass = QLineEdit()
        self.inp_confirm_pass.setEchoMode(QLineEdit.EchoMode.Password)

        btn_change_pass = QPushButton("Đổi Mật Khẩu")
        btn_change_pass.setStyleSheet("background-color:#e67e22;color:white;padding:8px;")
        btn_change_pass.clicked.connect(self.handle_change_pass)

        form_layout.addRow("User:", self.inp_username)
        form_layout.addRow("Pass cũ:", self.inp_old_pass)
        form_layout.addRow("Pass mới:", self.inp_new_pass)
        form_layout.addRow("Xác nhận:", self.inp_confirm_pass)
        form_layout.addRow("", btn_change_pass)

        group_auth.setLayout(form_layout)
        self.layout.addWidget(group_auth)

        self.layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    # ================= LOGIC =================

    def load_current_settings(self):
        if not self.current_user:
            return

        settings = self.settings_dao.get_settings_by_user(self.current_user["id"])
        if not settings:
            return

        self.inp_smtp_email.setText(settings["smtp_email"] or "")
        self.inp_smtp_pass.setText(settings["smtp_password"] or "")

    def handle_save_email_config(self):
        email = self.inp_smtp_email.text().strip()
        password = self.inp_smtp_pass.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đủ Email và Mật khẩu.")
            return

        success = self.settings_dao.update_email_settings(
            self.current_user["id"], email, password
        )

        if success:
            QMessageBox.information(self, "Thành công", "Đã lưu cấu hình Email!")
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể lưu vào Database.")

    def handle_change_pass(self):
        old = self.inp_old_pass.text()
        new = self.inp_new_pass.text()
        confirm = self.inp_confirm_pass.text()

        if not old or not new:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        if new != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp.")
            return

        success, msg = self.auth_controller.change_password(
            self.current_user["username"], old, new
        )

        if success:
            QMessageBox.information(self, "Thành công", msg)
            self.inp_old_pass.clear()
            self.inp_new_pass.clear()
            self.inp_confirm_pass.clear()
        else:
            QMessageBox.critical(self, "Thất bại", msg)
