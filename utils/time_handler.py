from datetime import datetime, timedelta

class TimeHandler:
    def add_days_to_current_date(self, days):
        time_delta = timedelta(days=days)
        now = datetime.today()
        new_date = now + time_delta
        return new_date

    def is_date_future(self, date):
        return datetime.today() < date
