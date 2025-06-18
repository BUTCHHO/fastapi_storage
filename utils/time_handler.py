from datetime import datetime, timedelta

class TimeHandler:
    def add_days_to_current_date(self, days):
        time_delta = timedelta(days=days)
        now = datetime.today()
        new_date = now + time_delta
        return new_date

    def is_date_future(self, date):
        return datetime.now().date() < date

    def get_today_date(self):
        return datetime.today()

    def get_str_today_date(self):
        return self.get_today_date().strftime('%d/%m/%Y')