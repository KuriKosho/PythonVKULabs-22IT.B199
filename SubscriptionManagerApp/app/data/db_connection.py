import sqlite3

from SubscriptionManagerApp.app.config import DB_PATH
from SubscriptionManagerApp.app.utils.security import hash_password


class Database:
    def __init__(self):
        self.db_path = DB_PATH

    def connect(self):
        """Tạo kết nối đến SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Để trả về kết quả dạng dict
        return conn

    def initialize_database(self):
        """Tạo bảng và dữ liệu mẫu nếu chưa tồn tại"""
        conn = self.connect()
        cursor = conn.cursor()

        # 1. Bảng Users (Quản trị viên)
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password_hash TEXT NOT NULL,
                            role TEXT DEFAULT 'admin',
                        
                            avatar_path TEXT,         
                            face_vector BLOB,          
                        
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                       ''')

        # 2. Bảng Members (Khách hàng)
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS members (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            full_name TEXT NOT NULL,
                            phone TEXT,
                            email TEXT,
                            address TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                        )
                       ''')

        # 3. Bảng Subscriptions (Gói đăng ký)
        cursor.execute('''
                      CREATE TABLE IF NOT EXISTS subscriptions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                    
                            user_id INTEGER NOT NULL,
                            member_id INTEGER NOT NULL,
                            plan_id INTEGER NOT NULL,
                    
                            price REAL NOT NULL,
                            start_date DATE NOT NULL,
                            end_date DATE NOT NULL,
                    
                            status TEXT DEFAULT 'Active',  -- Active, Paused, Overdue, Cancelled
                            note TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                            FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
                            FOREIGN KEY (plan_id) REFERENCES service_plans(id) ON DELETE CASCADE
                        )
                       ''')
        # 4. Bảng Service Plans (MỖI USER CÓ PLAN RIÊNG)
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS service_plans
                            (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                name TEXT NOT NULL,
                                duration_months INTEGER NOT NULL,
                                price REAL NOT NULL,
                                description TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        
                                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                            )
                       ''')

        # 5. Bảng Settings (Lưu cấu hình Email gửi thông báo)
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS system_settings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER UNIQUE NOT NULL,
                            smtp_email TEXT,
                            smtp_password TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                        );
                       ''')

        conn.commit()
        conn.close()
        print(f"✅ Kết nối Database thành công tại: {self.db_path}")


# Khởi tạo đối tượng DB để dùng chung
db = Database()