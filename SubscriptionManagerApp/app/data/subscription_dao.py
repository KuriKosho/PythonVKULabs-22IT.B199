from SubscriptionManagerApp.app.data.db_connection import db
from datetime import datetime


class SubscriptionDAO:

    # ================= QUERY =================
    def get_subscriptions_by_user(self, user_id):
        conn = db.connect()
        cursor = conn.cursor()

        query = """
            SELECT s.*, 
                   m.full_name,
                   p.name AS plan_name
            FROM subscriptions s
            JOIN members m ON s.member_id = m.id
            JOIN service_plans p ON s.plan_id = p.id
            WHERE s.user_id = ?
            ORDER BY s.end_date ASC
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        conn.close()
        return results

    # ================= ADD =================
    def add_subscription(self, user_id, member_id, plan_id, price, start_date, end_date, note):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO subscriptions
                (user_id, member_id, plan_id, price, start_date, end_date, status, note)
                VALUES (?, ?, ?, ?, ?, ?, 'Active', ?)
            """, (user_id, member_id, plan_id, price, start_date, end_date, note))
            conn.commit()
            return True
        except Exception as e:
            print("Add subscription error:", e)
            return False
        finally:
            conn.close()

    # ================= STATUS =================
    def update_status(self, sub_id, user_id, new_status):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE subscriptions
            SET status = ?
            WHERE id = ? AND user_id = ?
        """, (new_status, sub_id, user_id))
        conn.commit()
        conn.close()

    def check_and_update_overdue(self, user_id):
        conn = db.connect()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            UPDATE subscriptions
            SET status = 'Overdue'
            WHERE status = 'Active'
              AND end_date < ?
              AND user_id = ?
        """, (today, user_id))

        count = cursor.rowcount
        conn.commit()
        conn.close()
        return count

    # ================= DASHBOARD =================
    def get_dashboard_stats(self, user_id):
        conn = db.connect()
        cursor = conn.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) FROM members WHERE user_id = ?", (user_id,))
        stats["total_members"] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT SUM(price)
            FROM subscriptions
            WHERE status != 'Cancelled' AND user_id = ?
        """, (user_id,))
        stats["total_revenue"] = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT COUNT(*) FROM subscriptions
            WHERE status = 'Active' AND user_id = ?
        """, (user_id,))
        stats["active_subs"] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT status, COUNT(*)
            FROM subscriptions
            WHERE user_id = ?
            GROUP BY status
        """, (user_id,))
        stats["status_counts"] = cursor.fetchall()

        conn.close()
        return stats
