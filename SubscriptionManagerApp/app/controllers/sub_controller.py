from datetime import datetime
from SubscriptionManagerApp.app.data.subscription_dao import SubscriptionDAO
from SubscriptionManagerApp.app.utils.helpers import add_months


class SubController:
    def __init__(self):
        self.dao = SubscriptionDAO()

    def create_subscription(
        self,
        user_id,
        member_id,
        plan_id,
        price,
        duration_months,
        start_date_str,
        note
    ):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = add_months(start_date, duration_months)

        return self.dao.add_subscription(
            user_id,
            member_id,
            plan_id,
            price,
            start_date_str,
            end_date.strftime("%Y-%m-%d"),
            note
        )

    def refresh_statuses(self, user_id):
        return self.dao.check_and_update_overdue(user_id)
