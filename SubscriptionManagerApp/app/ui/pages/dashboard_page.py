from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QListWidget, QPushButton, QMessageBox,
    QFrame
)
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from SubscriptionManagerApp.app.data.subscription_dao import SubscriptionDAO
from SubscriptionManagerApp.app.ui.components.custom_card import CustomCard
from SubscriptionManagerApp.app.utils.helpers import format_currency
from SubscriptionManagerApp.app.utils.notification_service import NotificationService
from SubscriptionManagerApp.app.utils.section import Session


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.user = Session.get_user()
        if not self.user:
            raise RuntimeError("DashboardPage loaded without authenticated user")

        self.user_id = self.user["id"]
        self.dao = SubscriptionDAO()
        self.notif_service = NotificationService(self.user_id)

        self.init_ui()
        self.load_data()

    # =====================================================
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background:#f5f6fa;")

        content = QWidget()
        self.layout = QVBoxLayout(content)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # ===== HEADER =====
        lbl_title = QLabel("Dashboard")
        lbl_title.setStyleSheet("font-size:24px;font-weight:bold;color:#2c3e50;")

        lbl_sub = QLabel("Tổng quan hệ thống quản lý gói")
        lbl_sub.setStyleSheet("color:#7f8c8d;")

        self.layout.addWidget(lbl_title)
        self.layout.addWidget(lbl_sub)

        # ===== CARDS =====
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(15)
        self.layout.addLayout(self.cards_layout)

        # ===== MAIN CONTENT =====
        body_layout = QHBoxLayout()
        body_layout.setSpacing(15)

        # -------- LEFT: CHART AREA (70%) --------
        chart_frame = QFrame()
        chart_frame.setStyleSheet(
            "background:white;border-radius:8px;padding:15px;"
        )
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setSpacing(20)

        lbl_chart = QLabel("📊 Thống kê tổng quan")
        lbl_chart.setStyleSheet("font-weight:bold;font-size:16px;")
        chart_layout.addWidget(lbl_chart)

        charts_row = QHBoxLayout()
        charts_row.setSpacing(20)

        self.chart_left = QVBoxLayout()
        self.chart_right = QVBoxLayout()

        charts_row.addLayout(self.chart_left, 1)
        charts_row.addLayout(self.chart_right, 1)

        chart_layout.addLayout(charts_row)
        body_layout.addWidget(chart_frame, 3)

        # -------- RIGHT: SIDEBAR (30%) --------
        sidebar = QFrame()
        sidebar.setStyleSheet(
            "background:white;border-radius:8px;padding:15px;"
        )
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(10)

        lbl_notif = QLabel("🔔 Gói sắp hết hạn")
        lbl_notif.setStyleSheet(
            "font-weight:bold;font-size:15px;color:#e74c3c;"
        )

        self.list_notif = QListWidget()
        self.list_notif.setMinimumHeight(250)

        self.btn_send_mail = QPushButton("📧 Gửi Email nhắc nhở")
        self.btn_send_mail.clicked.connect(self.handle_send_mail)

        sidebar_layout.addWidget(lbl_notif)
        sidebar_layout.addWidget(self.list_notif)
        sidebar_layout.addWidget(self.btn_send_mail)

        body_layout.addWidget(sidebar, 1)

        self.layout.addLayout(body_layout)
        self.layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    # =====================================================
    def load_data(self):
        self.clear_layout(self.cards_layout)
        self.clear_layout(self.chart_left)
        self.clear_layout(self.chart_right)

        stats = self.dao.get_dashboard_stats(self.user_id)

        # ===== CARDS =====
        self.cards_layout.addWidget(
            CustomCard("👥 Thành viên", stats["total_members"], "#8e44ad")
        )
        self.cards_layout.addWidget(
            CustomCard("▶️ Gói hoạt động", stats["active_subs"], "#27ae60")
        )
        self.cards_layout.addWidget(
            CustomCard("💰 Doanh thu", format_currency(stats["total_revenue"]), "#2980b9")
        )
        self.cards_layout.addStretch()

        # ===== CHARTS =====
        self.chart_left.addWidget(self.create_pie_chart(stats["status_counts"]))
        self.chart_right.addWidget(self.create_bar_chart(stats["status_counts"]))

        # ===== SIDEBAR =====
        self.list_notif.clear()
        self.expiring_subs = self.notif_service.get_expiring_soon(days=3)

        if not self.expiring_subs:
            self.list_notif.addItem("Không có gói nào sắp hết hạn.")
            self.btn_send_mail.setEnabled(False)
        else:
            self.btn_send_mail.setEnabled(True)
            for sub in self.expiring_subs:
                self.list_notif.addItem(
                    f"{sub['full_name']} - {sub['plan_name']}\nHết hạn: {sub['end_date']}"
                )

    # =====================================================
    def create_pie_chart(self, data):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if not data:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha="center", va="center")
        else:
            labels = [row["status"] for row in data]
            values = [row[1] for row in data]
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title("Tỷ lệ trạng thái gói")

        return FigureCanvas(fig)

    def create_bar_chart(self, data):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if not data:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha="center", va="center")
        else:
            labels = [row["status"] for row in data]
            values = [row[1] for row in data]
            ax.bar(labels, values)
            ax.set_title("Số lượng gói theo trạng thái")

        return FigureCanvas(fig)

    # =====================================================
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # =====================================================
    def handle_send_mail(self):
        sent = 0
        for sub in self.expiring_subs:
            if sub["email"]:
                if self.notif_service.send_email_reminder(
                    sub["email"],
                    sub["full_name"],
                    sub["plan_name"],
                    sub["end_date"]
                ):
                    sent += 1

        QMessageBox.information(
            self, "Hoàn tất", f"Đã gửi {sent} email nhắc nhở."
        )
