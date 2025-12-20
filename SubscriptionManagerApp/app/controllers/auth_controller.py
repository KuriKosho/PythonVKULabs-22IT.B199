from SubscriptionManagerApp.app.data.user_dao import UserDAO
from SubscriptionManagerApp.app.utils.security import verify_password, hash_password
from SubscriptionManagerApp.app.data.db_connection import db
class AuthController:
    def __init__(self):
        self.dao = UserDAO()

    def login(self, username, password):
        """
        Kiểm tra đăng nhập.
        Return: User info (dict) nếu thành công, None nếu thất bại.
        """
        return self.dao.login(username, password)

    def register(self, username, password):
        """
        Đăng ký tài khoản mới.
        1. Kiểm tra user đã tồn tại chưa
        2. Hash mật khẩu
        3. Lưu user vào DB
        Return: User info (dict) nếu thành công, None nếu thất bại.
        """
        return self.dao.register(username, password)

    def change_password(self, username, old_pass, new_pass):
        """
        Đổi mật khẩu:
        1. Kiểm tra user tồn tại không
        2. Kiểm tra mật khẩu cũ đúng không
        3. Cập nhật mật khẩu mới (đã hash)
        """
        return self.dao.change_password(username, old_pass, new_pass)