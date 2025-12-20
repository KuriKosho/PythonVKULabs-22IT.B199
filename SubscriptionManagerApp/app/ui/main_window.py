from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from SubscriptionManagerApp.app.config import APP_NAME, WINDOW_SIZE
from SubscriptionManagerApp.app.ui.pages.dashboard_page import DashboardPage
from SubscriptionManagerApp.app.ui.pages.members_page import MembersPage
from SubscriptionManagerApp.app.ui.pages.plans_page import PlansPage
from SubscriptionManagerApp.app.ui.pages.settings_page import SettingsPage
from SubscriptionManagerApp.app.ui.pages.subs_page import SubsPage
from SubscriptionManagerApp.app.utils.section import Session


class MainWindow(QMainWindow):
    logoutRequested = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(*WINDOW_SIZE)

        self.init_ui()

    def init_ui(self):
        # Widget chính bao trùm toàn bộ cửa sổ
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout ngang: [ Sidebar | Content ]
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. SIDEBAR (Left) ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)

        # Logo / Title Sidebar
        lbl_logo = QLabel("SUB MANAGER")
        lbl_logo.setObjectName("SidebarLogo")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(lbl_logo)
        sidebar_layout.addSpacing(20)

        # Menu Buttons
        self.btn_dashboard = self.create_nav_btn("Dashboard")
        self.btn_subs = self.create_nav_btn("Subscription")
        self.btn_members = self.create_nav_btn("Members")
        self.btn_plans = self.create_nav_btn("Plans")
        self.btn_settings = self.create_nav_btn("Settings")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_subs)
        sidebar_layout.addWidget(self.btn_members)
        sidebar_layout.addWidget(self.btn_plans)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()  # Đẩy các nút lên trên

        # Logout Button (Bottom)
        btn_logout = QPushButton("Logout")
        btn_logout.setObjectName("BtnLogout")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.clicked.connect(self.handle_logout)
        sidebar_layout.addWidget(btn_logout)

        # --- 2. MAIN CONTENT (Right) ---
        self.content_area = QStackedWidget()

        # Tạo các trang
        self.page_dashboard = DashboardPage()
        self.page_subs = SubsPage()
        self.page_members = MembersPage()
        self.page_plans = PlansPage()
        self.page_settings = SettingsPage()

        # Thêm vào Stack
        self.content_area.addWidget(self.page_dashboard)  # Index 0
        self.content_area.addWidget(self.page_subs)  # Index 1
        self.content_area.addWidget(self.page_members)  # Index 2
        self.content_area.addWidget(self.page_plans)  # Index 3
        self.content_area.addWidget(self.page_settings)  # Index 4

        # Add Sidebar & Content to Main Layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)

        # Bắt sự kiện click menu
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_subs.clicked.connect(lambda: self.switch_page(1))
        self.btn_members.clicked.connect(lambda: self.switch_page(2))
        self.btn_plans.clicked.connect(lambda: self.switch_page(3))
        self.btn_settings.clicked.connect(lambda: self.switch_page(4))

        # Mặc định chọn Dashboard
        self.switch_page(0)
        self.btn_dashboard.clicked.connect(lambda: [self.switch_page(0), self.page_dashboard.load_data()])

    def create_nav_btn(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)  # Để giữ trạng thái active
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setObjectName("NavButton")
        return btn

    def switch_page(self, index):
        self.content_area.setCurrentIndex(index)

        # Cập nhật style cho nút đang chọn (Active State)
        buttons = [self.btn_dashboard, self.btn_subs, self.btn_members, self.btn_plans, self.btn_settings]
        for i, btn in enumerate(buttons):
            btn.setChecked(i == index)

    def handle_logout(self):
        Session.logout()
        self.logoutRequested.emit()
        self.close()
