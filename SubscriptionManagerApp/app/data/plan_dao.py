from SubscriptionManagerApp.app.data.db_connection import db


class PlanDAO:

    def get_plans_by_user(self, user_id: int):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM service_plans WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_plan(self, user_id: int, name, duration, price, desc):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO service_plans
                (user_id, name, duration_months, price, description)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, duration, price, desc))
            conn.commit()
            return True
        except Exception as e:
            print("Add plan error:", e)
            return False
        finally:
            conn.close()

    def update_plan(self, plan_id, user_id, name, duration, price, desc):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE service_plans
                       SET name            = ?,
                           duration_months = ?,
                           price           = ?,
                           description     = ?
                       WHERE id = ?
                         AND user_id = ?
                       """, (name, duration, price, desc, plan_id, user_id))
        conn.commit()
        conn.close()
        return True

    def delete_plan(self, plan_id, user_id):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM service_plans WHERE id = ? AND user_id = ?",
            (plan_id, user_id)
        )
        conn.commit()
        conn.close()
