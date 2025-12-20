from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QDialog, QFormLayout, QMessageBox,
    QComboBox, QDateEdit, QDoubleSpinBox, QLineEdit,
    QMenu, QFileDialog
)
from PyQt6.QtCore import Qt, QDate

from SubscriptionManagerApp.app.data.member_dao import MemberDAO
from SubscriptionManagerApp.app.data.subscription_dao import SubscriptionDAO
from SubscriptionManagerApp.app.controllers.sub_controller import SubController
from SubscriptionManagerApp.app.data.plan_dao import PlanDAO
from SubscriptionManagerApp.app.utils.helpers import format_currency, add_months
from SubscriptionManagerApp.app.utils.section import Session


# =====================================================
# ADD SUBSCRIPTION DIALOG
# =====================================================
class AddSubDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Đăng ký gói mới")
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

        btn_save = QPushButton("Lưu đăng ký")
        btn_save.clicked.connect(self.accept)
        layout.addWidget(btn_save)

        if self.plans:
            self.update_plan_info(0)

    # -------------------------------------------------
    def update_plan_info(self, index):
        plan = self.cb_plan.itemData(index)
        if not plan:
            return

        self.inp_price.setValue(plan["price"])
        self.selected_duration = plan["duration_months"]

    # -------------------------------------------------
    def get_data(self):
        return {
            "member_id": self.cb_member.currentData(),
            "plan_id": self.cb_plan.currentData()["id"],
            "plan_name": self.cb_plan.currentData()["name"],
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

        btn_refresh = QPushButton("Làm mới / Quét quá hạn")
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

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Khách hàng", "Gói", "Giá",
            "Ngày ĐK", "Hết hạn", "Trạng thái", "Ghi chú"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnHidden(0, True)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.table)

    # =================================================
    def load_data(self):
        # Quét quá hạn
        self.controller.refresh_statuses(self.user_id)

        subs = self.dao.get_subscriptions_by_user(self.user_id)
        self.table.setRowCount(0)

        for r, row in enumerate(subs):
            self.table.insertRow(r)

            self.table.setItem(r, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(row["full_name"]))
            self.table.setItem(r, 2, QTableWidgetItem(row["plan_name"]))
            self.table.setItem(r, 3, QTableWidgetItem(format_currency(row["price"])))
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

    # =================================================
    def refresh_data(self):
        self.load_data()
        QMessageBox.information(self, "OK", "Đã làm mới dữ liệu.")

    # =================================================
    def open_add_dialog(self):
        if not MemberDAO().get_members_by_user(self.user_id):
            QMessageBox.warning(
                self,
                "Thiếu dữ liệu",
                "Bạn cần thêm thành viên trước khi đăng ký gói."
            )
            return

        dialog = AddSubDialog(self.user_id, self)
        if dialog.exec():
            data = dialog.get_data()

            success = self.controller.create_subscription(
                self.user_id,
                data["member_id"],
                data["plan_id"],
                data["price"],
                data["duration"],
                data["start_date"],
                data["note"],
            )

            if success:
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã đăng ký gói!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể lưu dữ liệu.")

    # =================================================
    def show_context_menu(self, pos):
        index = self.table.indexAt(pos)
        if not index.isValid():
            return

        row = index.row()
        sub_id = int(self.table.item(row, 0).text())

        menu = QMenu()
        act_pause = menu.addAction("Tạm dừng")
        act_active = menu.addAction("Kích hoạt")
        act_cancel = menu.addAction("Hủy gói")

        action = menu.exec(self.table.viewport().mapToGlobal(pos))

        status_map = {
            act_pause: "Paused",
            act_active: "Active",
            act_cancel: "Cancelled",
        }

        if action in status_map:
            self.dao.update_status(sub_id, self.user_id, status_map[action])
            self.load_data()

    # =================================================
    def handle_export(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Xuất Excel",
            f"Subscriptions_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "Excel Files (*.xlsx)"
        )

        if path:
            success, msg = self.controller.export_to_excel(self.user_id, path)
            if success:
                QMessageBox.information(self, "OK", msg)
            else:
                QMessageBox.critical(self, "Lỗi", msg)
