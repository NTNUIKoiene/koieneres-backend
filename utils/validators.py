from datetime import timedelta, date, datetime
from utils.dateutils import string_to_date


def validate_selected_dates(selected_dates, is_cabin_board):
    '''
    Business rules for selected dates
    '''
    if len(selected_dates) == 0:
        return False
    if len(selected_dates) > 3 and not is_cabin_board:
        return False
    # Verify equal cabins
    names = list(map(lambda s: s['name'], selected_dates))
    if not names.count(names[0]) == len(names):
        return False
    dates = list(map(lambda s: string_to_date(s['date_key']), selected_dates))
    # Verify dates in future or now
    for date in dates:
        if date < datetime.now().date():
            return False
    # Verify sequential dates
    dates.sort()
    for i in range(len(dates) - 1):
        if not dates[i] - dates[i + 1] == timedelta(days=-1):
            return False

    return True
