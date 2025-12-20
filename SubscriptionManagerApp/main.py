import sys
import os
import traceback  # <--- Thêm thư viện này

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon

# Lưu ý: Đảm bảo import đúng đường dẫn tùy theo cách bạn chạy file
# Nếu chạy trực tiếp file main.py, có thể cần bỏ 'SubscriptionManagerApp.' ở đầu
try:
    from SubscriptionManagerApp.app.controllers.app_controller import AppController
    from SubscriptionManagerApp.app.data.db_connection import db
except ImportError:
    # Fallback nếu chạy tại thư mục gốc
    from app.controllers.app_controller import AppController
    from app.data.db_connection import db

def load_stylesheet(app):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Kiểm tra lại đường dẫn assets xem có đúng không
    qss_path = os.path.join(base_dir, "assets", "styles", "main.qss")

    if os.path.isfile(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

# --- HÀM BẮT LỖI TOÀN CỤC ---
def exception_hook(exctype, value, tb):
    """Bắt toàn bộ lỗi crash và in ra màn hình"""
    traceback.print_exception(exctype, value, tb)
    # Hiển thị popup lỗi để biết app đang crash vì lý do gì
    error_msg = "".join(traceback.format_exception(exctype, value, tb))
    print(error_msg)
    sys.exit(1)

def main():
    # Kích hoạt hàm bắt lỗi
    sys.excepthook = exception_hook

    # 1. Init database
    db.initialize_database()

    # 2. Init QApplication
    app = QApplication(sys.argv)

    # 3. App icon
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "icons", "app.ico")
    if os.path.isfile(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # 4. Load stylesheet
    load_stylesheet(app)

    # 5. Start App Controller
    controller = AppController()
    controller.start()

    # 6. Run event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()