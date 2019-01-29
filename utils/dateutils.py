from datetime import timedelta, date


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def compute_reservation_period(day=date.today()):
        offset = (day.weekday() - 2) % 7
        last_wednesday = day - timedelta(days=offset)
        period_duration = 15
        return {'from': last_wednesday, 'to': last_wednesday + timedelta(days=period_duration)}