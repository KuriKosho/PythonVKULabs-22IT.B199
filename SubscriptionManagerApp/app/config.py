import os

# Định vị thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Đường dẫn đến file Database
DB_PATH = os.path.join(BASE_DIR, "assets", "database", "app.db")

# Các hằng số khác
APP_NAME = "Subscription Manager"
WINDOW_SIZE = (1200, 720)
DATE_FORMAT = "%Y-%m-%d"