from datetime import date, datetime, timedelta

def today():
    return datetime.now().date()
def now():
    return datetime.now()
def this_year():
    return datetime.now().year()
def this_month():
    return date.month()
def this_week():
    return date.weekday()
def today_plus_year():
    return today() + timedelta(days=365)