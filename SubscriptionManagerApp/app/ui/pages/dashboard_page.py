from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QListWidget, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

# Matplotlib cho PyQt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# DAO & Utils
from SubscriptionManagerApp.app.data.subscription_dao import SubscriptionDAO
from SubscriptionManagerApp.app.ui.components.custom_card import CustomCard
from SubscriptionManagerApp.app.utils.helpers import format_currency
from SubscriptionManagerApp.app.utils.notification_service import NotificationService
from SubscriptionManagerApp.app.utils.section import Session


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        # ===== USER SESSION =====
        self.user = Session.get_user()
        if not self.user:
            raise RuntimeError("DashboardPage loaded without authenticated user")

        self.user_id = self.user["id"]

        # ===== SERVICES =====
        self.dao = SubscriptionDAO()
        self.notif_service = NotificationService(self.user_id)

        self.init_ui()

    # =====================================================
    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # Scroll (tránh vỡ layout màn hình nhỏ)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)

        # ===== TITLE =====
        lbl_title = QLabel("DASHBOARD OVERVIEW")
        lbl_title.setStyleSheet(
            "font-size:20px;font-weight:bold;color:#2c3e50;margin-bottom:10px;"
        )
        self.layout.addWidget(lbl_title)

        # ===== STATS CARDS =====
        self.stats_container = QHBoxLayout()
        self.layout.addLayout(self.stats_container)

        # ===== CHARTS =====
        self.charts_container = QHBoxLayout()
        self.layout.addLayout(self.charts_container)

        self.layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # ===== NOTIFICATION AREA =====
        lbl_notif = QLabel("🔔 Sắp hết hạn (3 ngày tới)")
        lbl_notif.setStyleSheet(
            "font-weight:bold;color:#e74c3c;margin-top:15px;"
        )
        main_layout.addWidget(lbl_notif)

        self.list_notif = QListWidget()
        self.list_notif.setMaximumHeight(150)
        main_layout.addWidget(self.list_notif)

        self.btn_send_mail = QPushButton("Gửi Email nhắc nhở")
        self.btn_send_mail.clicked.connect(self.handle_send_mail)
        main_layout.addWidget(self.btn_send_mail)

        self.load_data()

    # =====================================================
    def load_data(self):
        # Clear cũ
        self.clear_layout(self.stats_container)
        self.clear_layout(self.charts_container)

        # ===== LOAD STATS THEO USER =====
        stats = self.dao.get_dashboard_stats(self.user_id)

        # ===== CARDS =====
        card_members = CustomCard(
            "Tổng Thành Viên",
            stats["total_members"],
            color="#e67e22"
        )

        card_active = CustomCard(
            "Gói Đang Chạy",
            stats["active_subs"],
            color="#27ae60"
        )

        card_revenue = CustomCard(
            "Tổng Doanh Thu",
            format_currency(stats["total_revenue"]),
            color="#2980b9"
        )

        self.stats_container.addWidget(card_members)
        self.stats_container.addWidget(card_active)
        self.stats_container.addWidget(card_revenue)
        self.stats_container.addStretch()

        # ===== PIE CHART =====
        status_data = stats["status_counts"]

        if status_data:
            labels = []
            sizes = []
            colors = []

            color_map = {
                "Active": "#2ecc71",
                "Overdue": "#e74c3c",
                "Paused": "#f1c40f",
                "Cancelled": "#95a5a6",
            }

            for row in status_data:
                labels.append(f"{row['status']} ({row[1]})")
                sizes.append(row[1])
                colors.append(color_map.get(row["status"], "#34495e"))

            fig = Figure(figsize=(5, 4), dpi=100)
            fig.patch.set_facecolor("#ecf0f1")

            ax = fig.add_subplot(111)
            ax.pie(
                sizes,
                labels=labels,
                colors=colors,
                autopct="%1.1f%%",
                startangle=90
            )
            ax.set_title("Tỷ lệ Trạng thái Gói")

            canvas = FigureCanvas(fig)
            self.charts_container.addWidget(canvas)
        else:
            self.charts_container.addWidget(QLabel("Chưa có dữ liệu thống kê."))

        # ===== EXPIRING SOON =====
        self.list_notif.clear()
        self.expiring_subs = self.notif_service.get_expiring_soon(days=3)

        if not self.expiring_subs:
            self.list_notif.addItem("Không có gói nào sắp hết hạn.")
            self.btn_send_mail.setEnabled(False)
        else:
            self.btn_send_mail.setEnabled(True)
            for sub in self.expiring_subs:
                text = (
                    f"{sub['full_name']} - {sub['plan_name']} "
                    f"(Hết hạn: {sub['end_date']})"
                )
                self.list_notif.addItem(text)

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
            self,
            "Hoàn tất",
            f"Đã gửi thành công {sent} email nhắc nhở."
        )
