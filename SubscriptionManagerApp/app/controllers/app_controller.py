from SubscriptionManagerApp.app.ui.login_window import LoginWindow
from SubscriptionManagerApp.app.ui.main_window import MainWindow
from SubscriptionManagerApp.app.utils.section import Session


class AppController:
    def __init__(self):
        self.login_window = LoginWindow()
        self.main_window = None

        self.login_window.loginSuccess.connect(self.on_login)

    def start(self):
        try:
            self.login_window.show()
        except Exception as e:
            print("Error starting application:", e)

    def on_login(self):
        try:
            self.main_window = MainWindow()
            self.main_window.logoutRequested.connect(self.on_logout)

            self.main_window.show()
            self.login_window.close()
        except Exception as e:
            print("Error during login process:", e)

    def on_logout(self):
        try:
            Session.logout()
            self.main_window.close()
            self.main_window = None
            self.login_window.show()
        except Exception as e:
            print("Error during logout process:", e)
