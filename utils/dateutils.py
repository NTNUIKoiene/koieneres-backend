from datetime import date, datetime, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def compute_reservation_period(extensions, day=None):
    if day is None:
        day = date.today()
    current_extension = extensions.filter(reservation_date__lte=day, end_date__gte=day).order_by('-end_date').first()
    if current_extension is not None:
        return {
            "from": current_extension.reservation_date,
            "to": current_extension.end_date
        }
    offset = (day.weekday() - 2) % 7
    last_wednesday = day - timedelta(days=offset)
    period_duration = 15
    return {
        "from": last_wednesday,
        "to": last_wednesday + timedelta(days=period_duration),
    }


def string_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d").date()
