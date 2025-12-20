from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QDoubleSpinBox, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt

from SubscriptionManagerApp.app.data.plan_dao import PlanDAO
from SubscriptionManagerApp.app.utils.helpers import format_currency
from SubscriptionManagerApp.app.utils.section import Session


# =====================================================
# PLAN DIALOG (ADD / EDIT)
# =====================================================
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

        # EDIT MODE
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


# =====================================================
# PLANS PAGE
# =====================================================
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

    # =================================================
    def init_ui(self):
        layout = QVBoxLayout(self)

        # ===== HEADER =====
        top = QHBoxLayout()

        lbl = QLabel("QUẢN LÝ CÁC GÓI DỊCH VỤ")
        lbl.setStyleSheet("font-weight:bold; font-size:16px;")

        btn_add = QPushButton("+ Thêm Gói Mới")
        btn_add.setStyleSheet("background-color:#27ae60;color:white;padding:8px;")
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add.clicked.connect(lambda: self.open_edit_dialog())

        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(btn_add)
        layout.addLayout(top)

        # ===== SEARCH BAR =====
        search_bar = QHBoxLayout()

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍 Tìm theo tên gói hoặc mô tả...")
        self.inp_search.textChanged.connect(self.apply_filter)

        search_bar.addWidget(QLabel("Tìm kiếm:"))
        search_bar.addWidget(self.inp_search)

        layout.addLayout(search_bar)
        # ===== FILTER BAR =====
        filter_bar = QHBoxLayout()

        self.min_price = QDoubleSpinBox()
        self.min_price.setRange(0, 1_000_000_000)
        self.min_price.setSingleStep(50000)
        self.min_price.setPrefix("Từ ")

        self.max_price = QDoubleSpinBox()
        self.max_price.setRange(0, 1_000_000_000)
        self.max_price.setSingleStep(50000)
        self.max_price.setPrefix("Đến ")

        btn_clear = QPushButton("Xoá lọc")
        btn_clear.clicked.connect(self.clear_filters)

        # Trigger filter when changed
        self.min_price.valueChanged.connect(self.apply_filter)
        self.max_price.valueChanged.connect(self.apply_filter)

        filter_bar.addWidget(QLabel("Giá:"))
        filter_bar.addWidget(self.min_price)
        filter_bar.addWidget(self.max_price)
        filter_bar.addStretch()
        filter_bar.addWidget(btn_clear)

        layout.addLayout(filter_bar)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tên Gói", "Thời Hạn", "Giá", "Mô Tả", "Hành Động"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnHidden(0, True)
        self.table.setSortingEnabled(True)

        layout.addWidget(self.table)

    # =================================================
    def load_data(self):
        self.table.setSortingEnabled(False)
        plans = self.dao.get_plans_by_user(self.user_id)
        self.table.setRowCount(0)

        for r, row in enumerate(plans):
            self.table.insertRow(r)

            self.table.setItem(r, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(row["name"]))

            duration_item = QTableWidgetItem(f"{row['duration_months']} Tháng")
            duration_item.setData(Qt.ItemDataRole.UserRole, row["duration_months"])
            self.table.setItem(r, 2, duration_item)

            price_item = QTableWidgetItem(format_currency(row["price"]))
            price_item.setData(Qt.ItemDataRole.UserRole, row["price"])
            self.table.setItem(r, 3, price_item)

            self.table.setItem(r, 4, QTableWidgetItem(row["description"] or ""))

            # ===== ACTION BUTTONS =====
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

        self.table.setSortingEnabled(True)
        self.apply_filter()

    # =================================================
    def apply_filter(self):
        keyword = self.inp_search.text().lower()
        min_price = self.min_price.value()
        max_price = self.max_price.value()

        for row in range(self.table.rowCount()):
            name = self.table.item(row, 1).text().lower()
            desc = self.table.item(row, 4).text().lower()

            price_item = self.table.item(row, 3)
            price = price_item.data(Qt.ItemDataRole.UserRole)

            match_text = keyword in name or keyword in desc
            match_min = price >= min_price
            match_max = (max_price == 0 or price <= max_price)

            visible = match_text and match_min and match_max
            self.table.setRowHidden(row, not visible)

    # =================================================

    def clear_filters(self):
        self.inp_search.clear()
        self.min_price.setValue(0)
        self.max_price.setValue(0)
        self.apply_filter()


    def open_edit_dialog(self, plan=None):
        dialog = PlanDialog(self, plan)

        if dialog.exec():
            data = dialog.get_data()

            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên gói không được để trống")
                return

            if plan is None:
                self.dao.add_plan(
                    self.user_id,
                    data["name"],
                    data["duration"],
                    data["price"],
                    data["desc"]
                )
                QMessageBox.information(self, "OK", "Đã thêm gói mới!")
            else:
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

    # =================================================
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
