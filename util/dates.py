import datetime as dt

def days_to_date(start_dt: dt.datetime, days):
    return list(map(lambda delta_day: dt.timedelta(int(delta_day)) + start_dt, days.flatten()))