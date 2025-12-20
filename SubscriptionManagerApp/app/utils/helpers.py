from datetime import datetime
from dateutil.relativedelta import relativedelta

def add_months(start_date: datetime, months: int) -> datetime:
    """Cộng thêm số tháng vào ngày bắt đầu."""
    # Logic cộng tháng đơn giản
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1
    day = min(start_date.day, [31,
        29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return start_date.replace(year=year, month=month, day=day)

def format_currency(amount):
    """Format tiền VND: 100000 -> 100,000 VND"""
    return "{:,.0f} VND".format(amount)