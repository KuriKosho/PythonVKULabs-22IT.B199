from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QLabel, QDialog, QFormLayout, QMessageBox,
    QAbstractItemView, QCheckBox
)
from PyQt6.QtCore import Qt
from SubscriptionManagerApp.app.data.member_dao import MemberDAO
from SubscriptionManagerApp.app.utils.section import Session


# =====================================================
# MEMBER DIALOG
# =====================================================
class MemberDialog(QDialog):
    def __init__(self, parent=None, member_data=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin thành viên")
        self.setFixedSize(400, 300)
        self.member_data = member_data

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.inp_name = QLineEdit()
        self.inp_phone = QLineEdit()
        self.inp_email = QLineEdit()
        self.inp_address = QLineEdit()

        form.addRow("Họ tên (*):", self.inp_name)
        form.addRow("SĐT:", self.inp_phone)
        form.addRow("Email:", self.inp_email)
        form.addRow("Địa chỉ:", self.inp_address)

        layout.addLayout(form)

        btns = QHBoxLayout()
        btn_save = QPushButton("Lưu")
        btn_cancel = QPushButton("Huỷ")

        btn_save.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btns.addWidget(btn_save)
        btns.addWidget(btn_cancel)
        layout.addLayout(btns)

        if member_data:
            self.inp_name.setText(member_data["full_name"])
            self.inp_phone.setText(member_data["phone"])
            self.inp_email.setText(member_data["email"])
            self.inp_address.setText(member_data["address"])

    def get_data(self):
        return {
            "full_name": self.inp_name.text().strip(),
            "phone": self.inp_phone.text().strip(),
            "email": self.inp_email.text().strip(),
            "address": self.inp_address.text().strip(),
        }


# =====================================================
# MEMBERS PAGE
# =====================================================
class MembersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.user = Session.get_user()
        if not self.user:
            raise RuntimeError("MembersPage without login")

        self.user_id = self.user["id"]
        self.dao = MemberDAO()

        self.init_ui()
        self.load_data()

    # =================================================
    def init_ui(self):
        layout = QVBoxLayout(self)

        # ===== TOP BAR =====
        top = QHBoxLayout()
        lbl = QLabel("QUẢN LÝ THÀNH VIÊN")
        lbl.setStyleSheet("font-size:18px;font-weight:bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm theo tên / sđt / email")
        self.search_input.textChanged.connect(self.apply_filter)

        btn_add = QPushButton("+ Thêm mới")
        btn_add.setStyleSheet("background:#27ae60;color:white;padding:6px 15px;")
        btn_add.clicked.connect(self.open_add_dialog)

        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(self.search_input)
        top.addWidget(btn_add)
        layout.addLayout(top)

        # ===== FILTER BAR =====
        filter_bar = QHBoxLayout()

        self.chk_phone = QCheckBox("Có SĐT")
        self.chk_email = QCheckBox("Có Email")

        self.chk_phone.stateChanged.connect(self.apply_filter)
        self.chk_email.stateChanged.connect(self.apply_filter)

        filter_bar.addWidget(QLabel("Lọc:"))
        filter_bar.addWidget(self.chk_phone)
        filter_bar.addWidget(self.chk_email)
        filter_bar.addStretch()

        layout.addLayout(filter_bar)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Họ tên", "SĐT", "Email", "Địa chỉ", "Hành động"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setColumnHidden(0, True)

        layout.addWidget(self.table)

    # =================================================
    def load_data(self):
        self.table.setRowCount(0)
        members = self.dao.get_members_by_user(self.user_id)

        for r, m in enumerate(members):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(m["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(m["full_name"]))
            self.table.setItem(r, 2, QTableWidgetItem(m["phone"] or ""))
            self.table.setItem(r, 3, QTableWidgetItem(m["email"] or ""))
            self.table.setItem(r, 4, QTableWidgetItem(m["address"] or ""))

            # --- ACTION BUTTONS ---
            btn_edit = QPushButton("✏️")
            btn_delete = QPushButton("🗑️")

            btn_edit.clicked.connect(lambda _, row=m: self.open_edit_dialog(row))
            btn_delete.clicked.connect(lambda _, mid=m["id"]: self.confirm_delete(mid))

            action_layout = QHBoxLayout()
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.setContentsMargins(0, 0, 0, 0)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)

            self.table.setCellWidget(r, 5, action_widget)

        self.apply_filter()

    # =================================================
    def apply_filter(self):
        keyword = self.search_input.text().lower()
        filter_phone = self.chk_phone.isChecked()
        filter_email = self.chk_email.isChecked()

        for row in range(self.table.rowCount()):
            name = self.table.item(row, 1).text().lower()
            phone = self.table.item(row, 2).text()
            email = self.table.item(row, 3).text()

            match_text = (
                keyword in name or
                keyword in phone.lower() or
                keyword in email.lower()
            )

            match_phone = not filter_phone or bool(phone)
            match_email = not filter_email or bool(email)

            self.table.setRowHidden(
                row, not (match_text and match_phone and match_email)
            )

    # =================================================
    def open_add_dialog(self):
        dialog = MemberDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data["full_name"]:
                QMessageBox.warning(self, "Lỗi", "Họ tên không được trống")
                return

            self.dao.add_member(
                self.user_id,
                data["full_name"],
                data["phone"],
                data["email"],
                data["address"],
            )
            self.load_data()

    def open_edit_dialog(self, member):
        dialog = MemberDialog(self, member)
        if dialog.exec():
            data = dialog.get_data()
            self.dao.update_member(
                member["id"],
                self.user_id,
                data["full_name"],
                data["phone"],
                data["email"],
                data["address"],
            )
            self.load_data()

    def confirm_delete(self, member_id):
        reply = QMessageBox.question(
            self, "Xác nhận",
            "Bạn có chắc chắn muốn xoá thành viên này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.dao.delete_member(member_id, self.user_id)
            self.load_data()
