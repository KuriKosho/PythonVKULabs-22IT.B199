from SubscriptionManagerApp.app.data.db_connection import db
from SubscriptionManagerApp.app.utils.helpers import vector_to_blob
from SubscriptionManagerApp.app.utils.security import verify_password, hash_password


class UserDAO:
    def get_user_by_username(self, username):
        """Lấy thông tin user theo username"""
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def check_exits(self, username):
        """Kiểm tra user đã tồn tại chưa"""
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def login(self, username, plain_password):
        """Kiểm tra đăng nhập"""
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user:
            stored_hash = user['password_hash']
            if verify_password(plain_password, stored_hash):
                return user
        return None

    def register(self, username, password):
        """
        Đăng ký tài khoản mới.
        - Tạo user
        - Tạo system_settings (1-1)
        """
        conn = db.connect()
        cursor = conn.cursor()

        # 1. Kiểm tra user tồn tại
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return None

        password_hash = hash_password(password)

        try:
            # 2. Insert user
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )

            user_id = cursor.lastrowid  # 👈 ID user vừa tạo

            # 3. Insert system_settings mặc định cho user
            cursor.execute(
                "INSERT INTO system_settings (user_id) VALUES (?)",
                (user_id,)
            )

            # 4. Insert service_plans mặc định cho user
            default_plans = [
                (user_id, "Gói Cơ Bản (1 Tháng)", 1, 200000, "Gói trải nghiệm"),
                (user_id, "Gói Tiêu Chuẩn (3 Tháng)", 3, 550000, "Tiết kiệm hơn"),
                (user_id, "Gói VIP (1 Năm)", 12, 2000000, "Đầy đủ tính năng"),
            ]

            cursor.executemany("""
                               INSERT INTO service_plans
                                   (user_id, name, duration_months, price, description)
                               VALUES (?, ?, ?, ?, ?)
                               """, default_plans)

            conn.commit()

            # 5. Lấy lại user vừa tạo
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            return user

        except Exception as e:
            conn.rollback()
            print("Error during registration:", e)
            return None

        finally:
            conn.close()

    def change_password(self, username, old_pass, new_pass):
        """
        Đổi mật khẩu:
        1. Kiểm tra user tồn tại không
        2. Kiểm tra mật khẩu cũ đúng không
        3. Cập nhật mật khẩu mới (đã hash)
        """
        conn = db.connect()
        cursor = conn.cursor()

        # 1. Lấy thông tin user
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return False, "Tài khoản không tồn tại."

        # 2. Check pass cũ
        stored_hash = user['password_hash']
        if not verify_password(old_pass, stored_hash):
            conn.close()
            return False, "Mật khẩu cũ không đúng."

        # 3. Update pass mới
        new_hash = hash_password(new_pass)
        try:
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_hash, username))
            conn.commit()
            return True, "Đổi mật khẩu thành công!"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def update_user_face(self, user_id, avatar_path, face_vector):
        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE users
                       SET avatar_path = ?,
                           face_vector = ?
                       WHERE id = ?
                       """, (
                           avatar_path,
                           vector_to_blob(face_vector),
                           user_id
                       ))

        conn.commit()
        conn.close()


