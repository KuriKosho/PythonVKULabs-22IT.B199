from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QDialog, QFormLayout, QMessageBox,
    QComboBox, QDateEdit, QDoubleSpinBox, QLineEdit,
    QFileDialog
)
from PyQt6.QtCore import Qt, QDate

from SubscriptionManagerApp.app.data.member_dao import MemberDAO
from SubscriptionManagerApp.app.data.subscription_dao import SubscriptionDAO
from SubscriptionManagerApp.app.controllers.sub_controller import SubController
from SubscriptionManagerApp.app.data.plan_dao import PlanDAO
from SubscriptionManagerApp.app.utils.helpers import format_currency
from SubscriptionManagerApp.app.utils.section import Session


# =====================================================
# ADD / EDIT SUBSCRIPTION DIALOG
# =====================================================
class AddSubDialog(QDialog):
    def __init__(self, user_id, parent=None, subscription=None):
        super().__init__(parent)
        self.user_id = user_id
        self.subscription = subscription

        self.setWindowTitle(
            "Chỉnh sửa đăng ký" if subscription else "Đăng ký gói mới"
        )
        self.setFixedSize(450, 400)

        self.member_dao = MemberDAO()
        self.plan_dao = PlanDAO()
        self.selected_duration = 1

        layout = QVBoxLayout(self)
        form = QFormLayout()

        # ===== MEMBER =====
        self.cb_member = QComboBox()
        self.members = self.member_dao.get_members_by_user(user_id)
        for m in self.members:
            self.cb_member.addItem(
                f"{m['full_name']} - {m['phone']}", m["id"]
            )

        # ===== PLAN =====
        self.cb_plan = QComboBox()
        self.plans = self.plan_dao.get_plans_by_user(user_id)
        for p in self.plans:
            self.cb_plan.addItem(p["name"], p)

        self.cb_plan.currentIndexChanged.connect(self.update_plan_info)

        # ===== PRICE =====
        self.inp_price = QDoubleSpinBox()
        self.inp_price.setRange(0, 1_000_000_000)
        self.inp_price.setSingleStep(50000)

        # ===== START DATE =====
        self.inp_start_date = QDateEdit()
        self.inp_start_date.setCalendarPopup(True)
        self.inp_start_date.setDate(QDate.currentDate())
        self.inp_start_date.setDisplayFormat("yyyy-MM-dd")

        # ===== NOTE =====
        self.inp_note = QLineEdit()

        form.addRow("Khách hàng (*):", self.cb_member)
        form.addRow("Gói dịch vụ (*):", self.cb_plan)
        form.addRow("Giá tiền:", self.inp_price)
        form.addRow("Ngày bắt đầu:", self.inp_start_date)
        form.addRow("Ghi chú:", self.inp_note)

        layout.addLayout(form)

        btn_save = QPushButton("Lưu")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        # ===== EDIT MODE =====
        if subscription:
            self.load_subscription(subscription)
        elif self.plans:
            self.update_plan_info(0)

    # -------------------------------------------------
    def load_subscription(self, sub):
        self.cb_member.setCurrentIndex(
            self.cb_member.findData(sub["member_id"])
        )

        for i in range(self.cb_plan.count()):
            if self.cb_plan.itemData(i)["id"] == sub["plan_id"]:
                self.cb_plan.setCurrentIndex(i)
                break

        self.inp_price.setValue(sub["price"])
        self.inp_start_date.setDate(
            QDate.fromString(sub["start_date"], "yyyy-MM-dd")
        )
        self.inp_note.setText(sub["note"] or "")

    # -------------------------------------------------
    def update_plan_info(self, index):
        plan = self.cb_plan.itemData(index)
        if plan:
            self.inp_price.setValue(plan["price"])
            self.selected_duration = plan["duration_months"]

    # -------------------------------------------------
    def get_data(self):
        return {
            "member_id": self.cb_member.currentData(),
            "plan_id": self.cb_plan.currentData()["id"],
            "price": self.inp_price.value(),
            "start_date": self.inp_start_date.date().toString("yyyy-MM-dd"),
            "duration": self.selected_duration,
            "note": self.inp_note.text().strip(),
        }


# =====================================================
# SUBSCRIPTIONS PAGE
# =====================================================
class SubsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.user = Session.get_user()
        if not self.user:
            raise RuntimeError("SubsPage loaded without authenticated user")

        self.user_id = self.user["id"]
        self.dao = SubscriptionDAO()
        self.controller = SubController()

        self.init_ui()
        self.load_data()

    # =================================================
    def init_ui(self):
        layout = QVBoxLayout(self)

        # ===== TOP BAR =====
        top = QHBoxLayout()

        lbl = QLabel("QUẢN LÝ GÓI ĐĂNG KÝ (SUBSCRIPTION)")
        lbl.setStyleSheet("font-size:18px;font-weight:bold;")

        btn_add = QPushButton("+ Đăng ký mới")
        btn_add.setStyleSheet("background:#3498db;color:white;padding:6px 15px;")
        btn_add.clicked.connect(self.open_add_dialog)

        btn_refresh = QPushButton("Làm mới")
        btn_refresh.clicked.connect(self.refresh_data)

        btn_export = QPushButton("Xuất Excel")
        btn_export.setStyleSheet("background:#2ecc71;color:white;padding:6px 15px;")
        btn_export.clicked.connect(self.handle_export)

        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(btn_refresh)
        top.addWidget(btn_add)
        top.addWidget(btn_export)
        layout.addLayout(top)

        # ===== SEARCH PANEL =====
        search_bar = QHBoxLayout()

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍 Tìm khách hàng / gói / ghi chú...")
        self.inp_search.textChanged.connect(self.apply_filters)

        self.cb_status = QComboBox()
        self.cb_status.addItems(["Tất cả", "Active", "Overdue", "Paused"])
        self.cb_status.currentIndexChanged.connect(self.apply_filters)

        self.cb_plan = QComboBox()
        self.cb_plan.addItem("Tất cả gói")
        self.cb_plan.currentIndexChanged.connect(self.apply_filters)

        search_bar.addWidget(QLabel("Tìm:"))
        search_bar.addWidget(self.inp_search, 2)
        search_bar.addWidget(QLabel("Trạng thái:"))
        search_bar.addWidget(self.cb_status)
        search_bar.addWidget(QLabel("Gói:"))
        search_bar.addWidget(self.cb_plan)

        layout.addLayout(search_bar)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Khách hàng", "Gói", "Giá",
            "Ngày ĐK", "Hết hạn", "Trạng thái",
            "Ghi chú", "Hành động"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnHidden(0, True)
        self.table.setSortingEnabled(True)

        layout.addWidget(self.table)

    # =================================================
    def load_data(self):
        self.table.setSortingEnabled(False)

        self.controller.refresh_statuses(self.user_id)
        subs = self.dao.get_subscriptions_by_user(self.user_id)
        self.table.setRowCount(0)

        plans_set = set()

        for r, row in enumerate(subs):
            self.table.insertRow(r)

            self.table.setItem(r, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(row["full_name"]))
            self.table.setItem(r, 2, QTableWidgetItem(row["plan_name"]))
            plans_set.add(row["plan_name"])

            price_item = QTableWidgetItem(format_currency(row["price"]))
            price_item.setData(Qt.ItemDataRole.UserRole, row["price"])
            self.table.setItem(r, 3, price_item)

            self.table.setItem(r, 4, QTableWidgetItem(row["start_date"]))
            self.table.setItem(r, 5, QTableWidgetItem(row["end_date"]))

            status_item = QTableWidgetItem(row["status"])
            if row["status"] == "Active":
                status_item.setForeground(Qt.GlobalColor.darkGreen)
            elif row["status"] == "Overdue":
                status_item.setForeground(Qt.GlobalColor.red)
            elif row["status"] == "Paused":
                status_item.setForeground(Qt.GlobalColor.darkYellow)
            self.table.setItem(r, 6, status_item)

            self.table.setItem(r, 7, QTableWidgetItem(row["note"] or ""))

            # ACTION
            btn_edit = QPushButton("✏️")
            btn_delete = QPushButton("🗑️")
            btn_edit.clicked.connect(lambda _, s=row: self.open_edit_dialog(s))
            btn_delete.clicked.connect(lambda _, sid=row["id"]: self.confirm_delete(sid))

            action_layout = QHBoxLayout()
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.setContentsMargins(0, 0, 0, 0)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(r, 8, action_widget)

        # Update plan filter
        self.cb_plan.blockSignals(True)
        self.cb_plan.clear()
        self.cb_plan.addItem("Tất cả gói")
        for p in sorted(plans_set):
            self.cb_plan.addItem(p)
        self.cb_plan.blockSignals(False)

        self.table.setSortingEnabled(True)
        self.apply_filters()

    # =================================================
    def apply_filters(self):
        text = self.inp_search.text().lower()
        status = self.cb_status.currentText()
        plan = self.cb_plan.currentText()

        for row in range(self.table.rowCount()):
            match = True

            customer = self.table.item(row, 1).text().lower()
            plan_name = self.table.item(row, 2).text().lower()
            note = self.table.item(row, 7).text().lower()
            row_status = self.table.item(row, 6).text()

            if text and text not in customer and text not in plan_name and text not in note:
                match = False

            if status != "Tất cả" and row_status != status:
                match = False

            if plan != "Tất cả gói" and self.table.item(row, 2).text() != plan:
                match = False

            self.table.setRowHidden(row, not match)

    # =================================================
    def open_add_dialog(self):
        dialog = AddSubDialog(self.user_id, self)
        if dialog.exec():
            data = dialog.get_data()
            self.controller.create_subscription(
                self.user_id,
                data["member_id"],
                data["plan_id"],
                data["price"],
                data["duration"],
                data["start_date"],
                data["note"],
            )
            self.load_data()

    def open_edit_dialog(self, subscription):
        dialog = AddSubDialog(self.user_id, self, subscription)
        if dialog.exec():
            data = dialog.get_data()
            self.dao.update_subscription(
                subscription["id"],
                self.user_id,
                data["member_id"],
                data["plan_id"],
                data["price"],
                data["start_date"],
                data["duration"],
                data["note"],
            )
            self.load_data()

    def confirm_delete(self, sub_id):
        reply = QMessageBox.question(
            self, "Xác nhận",
            "Bạn có chắc chắn muốn xoá đăng ký này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.dao.delete_subscription(sub_id, self.user_id)
            self.load_data()

    def refresh_data(self):
        self.load_data()

    def handle_export(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Xuất Excel",
            f"Subscriptions_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "Excel Files (*.xlsx)"
        )
        if path:
            self.controller.export_to_excel(self.user_id, path)

