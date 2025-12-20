from SubscriptionManagerApp.app.data.db_connection import db


class SettingsDAO:
    def get_settings_by_user(self, user_id):
        """Lấy settings theo user_id"""
        conn = db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM system_settings WHERE user_id = ?",
            (user_id,)
        )
        settings = cursor.fetchone()
        conn.close()
        return settings

    def update_email_settings(self, user_id, smtp_email, smtp_password):
        """Cập nhật SMTP settings cho user"""
        conn = db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE system_settings
                SET smtp_email = ?, smtp_password = ?
                WHERE user_id = ?
            """, (smtp_email, smtp_password, user_id))
            conn.commit()
            return True
        except Exception as e:
            print("Lỗi lưu email settings:", e)
            conn.rollback()
            return False
        finally:
            conn.close()
