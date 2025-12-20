from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QLineEdit, QLabel, QDialog, QFormLayout, QMessageBox, QAbstractItemView)
from PyQt6.QtCore import Qt
from SubscriptionManagerApp.app.data.member_dao import MemberDAO
from SubscriptionManagerApp.app.utils.section import Session


class MemberDialog(QDialog):
    """Dialog dùng chung cho việc Thêm mới và Sửa"""

    def __init__(self, parent=None, member_data=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin thành viên")
        self.setFixedSize(400, 300)
        self.member_data = member_data
        self.layout = QVBoxLayout(self)

        # Form inputs
        form_layout = QFormLayout()
        self.inp_name = QLineEdit()
        self.inp_phone = QLineEdit()
        self.inp_email = QLineEdit()
        self.inp_address = QLineEdit()

        form_layout.addRow("Họ tên (*):", self.inp_name)
        form_layout.addRow("Số điện thoại:", self.inp_phone)
        form_layout.addRow("Email:", self.inp_email)
        form_layout.addRow("Địa chỉ:", self.inp_address)

        self.layout.addLayout(form_layout)

        # Buttons
        btn_box = QHBoxLayout()
        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        btn_box.addWidget(self.btn_save)
        btn_box.addWidget(self.btn_cancel)
        self.layout.addLayout(btn_box)

        # Nếu là chế độ Edit -> Điền dữ liệu cũ
        if self.member_data:
            self.inp_name.setText(str(self.member_data['full_name']))
            self.inp_phone.setText(str(self.member_data['phone']))
            self.inp_email.setText(str(self.member_data['email']))
            self.inp_address.setText(str(self.member_data['address']))

    def get_data(self):
        return {
            "full_name": self.inp_name.text(),
            "phone": self.inp_phone.text(),
            "email": self.inp_email.text(),
            "address": self.inp_address.text()
        }


class MembersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.current_user = Session.get_user()
        if not self.current_user:
            raise RuntimeError("MembersPage loaded without authenticated user")

        self.user_id = self.current_user["id"]
        self.dao = MemberDAO()

        self.init_ui()
        self.load_data()


    def init_ui(self):
        layout = QVBoxLayout(self)

        # --- TOP BAR (Title + Search + Add Button) ---
        top_bar = QHBoxLayout()

        lbl_title = QLabel("DANH SÁCH THÀNH VIÊN")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên, sđt...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.load_data)  # Auto search khi gõ

        btn_add = QPushButton("+ Thêm mới")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.setStyleSheet("background-color: #27ae60; color: white; padding: 5px 15px; border-radius: 4px;")
        btn_add.clicked.connect(self.open_add_dialog)

        top_bar.addWidget(lbl_title)
        top_bar.addStretch()
        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_add)

        layout.addLayout(top_bar)

        # --- TABLE ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Họ Tên", "SĐT", "Email", "Địa chỉ", "Hành động"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # Chọn cả dòng
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Không cho sửa trực tiếp trên bảng

        # Ẩn cột ID (cột 0) vì user ko cần thấy
        self.table.setColumnHidden(0, True)

        # Sự kiện click đúp để sửa
        self.table.doubleClicked.connect(self.open_edit_dialog)

        layout.addWidget(self.table)

    def load_data(self):
        keyword = self.search_input.text().strip()

        if keyword:
            data = self.dao.search_members(self.user_id, keyword)
        else:
            data = self.dao.get_members_by_user(self.user_id)

        self.table.setRowCount(0)
        for row_idx, row in enumerate(data):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row['full_name']))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row['phone'] or ""))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row['email'] or ""))
            self.table.setItem(row_idx, 4, QTableWidgetItem(row['address'] or ""))
            self.table.setItem(row_idx, 5, QTableWidgetItem("Double click để sửa"))

    def open_add_dialog(self):
        dialog = MemberDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data['full_name']:
                QMessageBox.warning(self, "Lỗi", "Họ tên không được để trống!")
                return

            ok = self.dao.add_member(
                self.user_id,
                data['full_name'],
                data['phone'],
                data['email'],
                data['address']
            )

            if ok:
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã thêm thành viên!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể thêm thành viên.")

    def open_edit_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            return

        member_id = int(self.table.item(row, 0).text())

        current_data = {
            "full_name": self.table.item(row, 1).text(),
            "phone": self.table.item(row, 2).text(),
            "email": self.table.item(row, 3).text(),
            "address": self.table.item(row, 4).text(),
        }

        dialog = MemberDialog(self, member_data=current_data)
        if dialog.exec():
            data = dialog.get_data()
            ok = self.dao.update_member(
                member_id,
                self.user_id,
                data['full_name'],
                data['phone'],
                data['email'],
                data['address']
            )

            if ok:
                self.load_data()
                QMessageBox.information(self, "OK", "Cập nhật thành công!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể cập nhật.")
