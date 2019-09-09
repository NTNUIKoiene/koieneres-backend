from datetime import date, datetime, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def compute_reservation_period(day=None):
    if day is None:
        day = date.today()
    offset = (day.weekday() - 2) % 7
    last_wednesday = day - timedelta(days=offset)
    period_duration = 15
    return {
        "from": last_wednesday,
        "to": last_wednesday + timedelta(days=period_duration),
    }


def string_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d").date()
