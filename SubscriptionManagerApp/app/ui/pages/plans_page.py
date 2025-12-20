from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QDialog, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from SubscriptionManagerApp.app.data.plan_dao import PlanDAO
from SubscriptionManagerApp.app.utils.helpers import format_currency
from SubscriptionManagerApp.app.utils.section import Session


class PlanDialog(QDialog):
    def __init__(self, parent=None, plan=None):
        super().__init__(parent)
        self.plan = plan
        self.setWindowTitle("Thông tin Gói dịch vụ")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.inp_name = QLineEdit()
        self.inp_duration = QSpinBox()
        self.inp_duration.setRange(1, 100)
        self.inp_duration.setSuffix(" Tháng")

        self.inp_price = QDoubleSpinBox()
        self.inp_price.setRange(0, 1_000_000_000)
        self.inp_price.setSingleStep(50000)

        self.inp_desc = QLineEdit()

        form.addRow("Tên Gói:", self.inp_name)
        form.addRow("Thời hạn:", self.inp_duration)
        form.addRow("Giá:", self.inp_price)
        form.addRow("Mô tả:", self.inp_desc)

        layout.addLayout(form)

        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        # Nếu là EDIT → đổ dữ liệu
        if self.plan:
            self.inp_name.setText(self.plan["name"])
            self.inp_duration.setValue(self.plan["duration_months"])
            self.inp_price.setValue(self.plan["price"])
            self.inp_desc.setText(self.plan["description"] or "")

    def get_data(self):
        return {
            "name": self.inp_name.text().strip(),
            "duration": self.inp_duration.value(),
            "price": self.inp_price.value(),
            "desc": self.inp_desc.text().strip()
        }



class PlansPage(QWidget):
    def __init__(self):
        super().__init__()

        self.current_user = Session.get_user()
        if not self.current_user:
            raise RuntimeError("PlansPage loaded without authenticated user")

        self.user_id = self.current_user["id"]
        self.dao = PlanDAO()

        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        top = QHBoxLayout()
        top.addWidget(QLabel("QUẢN LÝ CÁC GÓI DỊCH VỤ", styleSheet="font-weight:bold; font-size:16px;"))
        btn_add = QPushButton("+ Thêm Gói Mới")
        btn_add.setStyleSheet("background-color:#27ae60;color:white;padding:8px;")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(lambda: self.open_edit_dialog())
        top.addWidget(btn_add)
        layout.addLayout(top)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên Gói", "Thời Hạn", "Giá", "Mô Tả", "Hành Động"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnHidden(0, True)
        layout.addWidget(self.table)

    def load_data(self):
        plans = self.dao.get_plans_by_user(self.user_id)
        self.table.setRowCount(0)

        for r, row in enumerate(plans):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(row['id'])))
            self.table.setItem(r, 1, QTableWidgetItem(row['name']))
            self.table.setItem(r, 2, QTableWidgetItem(f"{row['duration_months']} Tháng"))
            self.table.setItem(r, 3, QTableWidgetItem(format_currency(row['price'])))
            self.table.setItem(r, 4, QTableWidgetItem(row['description'] or ""))

            # --- ACTION BUTTONS ---
            btn_edit = QPushButton("✏️")
            btn_delete = QPushButton("🗑️")

            btn_edit.clicked.connect(lambda _, p=row: self.open_edit_dialog(p))
            btn_delete.clicked.connect(lambda _, pid=row["id"]: self.confirm_delete(pid))

            action_layout = QHBoxLayout()
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.setContentsMargins(0, 0, 0, 0)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)

            self.table.setCellWidget(r, 5, action_widget)

    def open_edit_dialog(self, plan=None):
        dialog = PlanDialog(self, plan)

        if dialog.exec():
            data = dialog.get_data()

            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên gói không được để trống")
                return

            if plan is None:
                # 👉 ADD NEW
                self.dao.add_plan(
                    self.user_id,
                    data["name"],
                    data["duration"],
                    data["price"],
                    data["desc"]
                )
                QMessageBox.information(self, "OK", "Đã thêm gói mới!")
            else:
                # 👉 UPDATE
                self.dao.update_plan(
                    plan["id"],
                    self.user_id,
                    data["name"],
                    data["duration"],
                    data["price"],
                    data["desc"]
                )
                QMessageBox.information(self, "OK", "Đã cập nhật gói!")

            self.load_data()

    def confirm_delete(self, plan_id):
        reply = QMessageBox.question(
            self,
            "Xác nhận xoá",
            "Bạn có chắc chắn muốn xoá gói này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.dao.delete_plan(plan_id, self.user_id)
            self.load_data()
            QMessageBox.information(self, "OK", "Đã xoá gói!")

