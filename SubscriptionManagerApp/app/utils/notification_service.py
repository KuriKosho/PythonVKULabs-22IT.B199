import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from SubscriptionManagerApp.app.data.db_connection import db
from SubscriptionManagerApp.app.data.settings_dao import SettingsDAO


class NotificationService:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.settings_dao = SettingsDAO()

    # =================================================
    # LẤY DANH SÁCH SẮP HẾT HẠN (THEO USER)
    # =================================================
    def get_expiring_soon(self, days=3):
        conn = db.connect()
        cursor = conn.cursor()

        today = datetime.now().strftime("%Y-%m-%d")
        target_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

        query = """
                SELECT s.id, \
                       sp.name AS plan_name, \
                       s.end_date, \
                       m.full_name, \
                       m.email
                FROM subscriptions s
                         JOIN members m ON s.member_id = m.id
                         JOIN service_plans sp ON s.plan_id = sp.id
                WHERE s.user_id = ?
                  AND s.status = 'Active'
                  AND s.end_date BETWEEN ? AND ?
                ORDER BY s.end_date ASC \
                """

        cursor.execute(query, (self.user_id, today, target_date))
        rows = cursor.fetchall()
        conn.close()
        return rows

    # =================================================
    # GỬI EMAIL NHẮC NHỞ
    # =================================================
    def send_email_reminder(self, to_email, member_name, plan_name, end_date):
        """
        Gửi email nhắc nhở gia hạn
        Email gửi đi lấy từ system_settings của user
        """

        # 1. Lấy cấu hình SMTP theo USER
        sender_email = self.settings_dao.get_setting(self.user_id, "smtp_email")
        sender_password = self.settings_dao.get_setting(self.user_id, "smtp_password")

        if not sender_email or not sender_password:
            print("❌ Chưa cấu hình Email SMTP cho user:", self.user_id)
            return False

        subject = f"Nhắc nhở gia hạn dịch vụ - {plan_name}"
        body = f"""
Xin chào {member_name},

Gói dịch vụ "{plan_name}" của bạn sẽ hết hạn vào ngày {end_date}.

Vui lòng liên hệ để gia hạn nhằm tránh gián đoạn dịch vụ.

Trân trọng,
Subscription Manager App
"""

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)

            print(f"✅ Đã gửi mail tới {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("❌ Sai Email hoặc App Password SMTP")
            return False

        except Exception as e:
            print("❌ Lỗi gửi mail:", e)
            return False
