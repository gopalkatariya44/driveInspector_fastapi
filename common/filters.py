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
    value_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    utc_timezone = pytz.timezone('UTC')
    target_timezone = pytz.timezone(target_timezone)
    value_utc = utc_timezone.localize(value_datetime)
    value_local = value_utc.astimezone(target_timezone)
    return value_local.strftime('%d %b %Y')


def is_date_expired(value_str, target_timezone):
    value = datetime.strptime(value_str, "%Y-%m-%dT%H:%M:%SZ")
    local_timezone = pytz.timezone(target_timezone)
    value_local = value.astimezone(local_timezone)
    today_local = datetime.now(local_timezone).date()
    return today_local < value_local.date()


# Add the custom filter to the Jinja2 environment
templates.env.filters['convert_timezone'] = convert_timezone
templates.env.filters['convert_timezone_date'] = convert_timezone_date
templates.env.filters['is_date_expired'] = is_date_expired
