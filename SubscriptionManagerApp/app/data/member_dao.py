from SubscriptionManagerApp.app.data.db_connection import db


class MemberDAO:

    def get_members_by_user(self, user_id):
        """Lấy danh sách member của user"""
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM members WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_member(self, user_id, full_name, phone, email, address):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO members (user_id, full_name, phone, email, address)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, full_name, phone, email, address))
            conn.commit()
            return True
        except Exception as e:
            print("Error adding member:", e)
            return False
        finally:
            conn.close()

    def update_member(self, member_id, user_id, full_name, phone, email, address):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE members
                SET full_name = ?, phone = ?, email = ?, address = ?
                WHERE id = ? AND user_id = ?
            """, (full_name, phone, email, address, member_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error updating member:", e)
            return False
        finally:
            conn.close()

    def delete_member(self, member_id, user_id):
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM members WHERE id = ? AND user_id = ?",
                (member_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Error deleting member:", e)
            return False
        finally:
            conn.close()

    def search_members(self, user_id, keyword):
        conn = db.connect()
        cursor = conn.cursor()
        pattern = f"%{keyword}%"
        cursor.execute("""
            SELECT *
            FROM members
            WHERE user_id = ?
              AND (full_name LIKE ? OR phone LIKE ? OR email LIKE ?)
            ORDER BY id DESC
        """, (user_id, pattern, pattern, pattern))
        rows = cursor.fetchall()
        conn.close()
        return rows
