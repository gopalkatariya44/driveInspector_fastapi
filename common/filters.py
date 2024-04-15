from datetime import datetime
import pytz
from features import templates


def convert_timezone(value, target_timezone):
    utc_timezone = pytz.timezone('UTC')
    target_timezone = pytz.timezone(target_timezone)
    value_utc = utc_timezone.localize(value)
    value_local = value_utc.astimezone(target_timezone)
    return value_local.strftime('%d %b %Y %I:%M %p')


def convert_timezone_date(value, target_timezone):
    utc_timezone = pytz.timezone('UTC')
    target_timezone = pytz.timezone(target_timezone)
    value_utc = utc_timezone.localize(value)
    value_local = value_utc.astimezone(target_timezone)
    return value_local.strftime('%d %b %Y')


# def is_date_expired(value):
#     date_string = '2022-04-08 15:30:00'
#     parsed_date = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
#     date_format = '%Y-%m-%dT%H:%M:%SZ'
#     today = datetime.now().date()
#     return today < datetime.strptime(parsed_date, date_format).date()

def is_date_expired(value, target_timezone):
    # Convert UTC time to local time
    local_timezone = pytz.timezone(target_timezone)  # Specify your local timezone
    value_local = value.astimezone(local_timezone)

    # Get today's date in local time
    today_local = datetime.now(local_timezone).date()

    # Compare the local time with today's date
    return today_local < value_local.date()


# Add the custom filter to the Jinja2 environment
templates.env.filters['convert_timezone'] = convert_timezone
templates.env.filters['convert_timezone_date'] = convert_timezone_date

templates.env.filters['is_date_expired'] = is_date_expired
