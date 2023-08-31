import datetime
from calendar import monthrange
from pytz import timezone
from all_config import getconfigs


def content_maker(days_before: int = 3, days_after: int = 11):
    now = datetime.datetime.now(tz).date()
    first_day_of_range = now - datetime.timedelta(days=days_before)
    last_day_of_range = now + datetime.timedelta(days=days_after)
    first_day_of_range_tup = (first_day_of_range.year,
                              first_day_of_range.month, first_day_of_range.day)
    last_day_of_range_tup = (last_day_of_range.year,
                             last_day_of_range.month, last_day_of_range.day)
    return first_day_of_range_tup, last_day_of_range_tup


def this_week():
    now = datetime.datetime.now(tz)
    first_day_of_week = now - datetime.timedelta(days=(now.weekday()+1) % 7)
    last_day_of_week = first_day_of_week + datetime.timedelta(days=6)
    first_day_of_week = tz.localize(
        first_day_of_week.combine(first_day_of_week, datetime.time.min))
    last_day_of_week = tz.localize(
        last_day_of_week.combine(last_day_of_week, datetime.time.max))
    timestamp_first_day_of_week = int(first_day_of_week.timestamp())
    timestamp_last_day_of_week = int(last_day_of_week.timestamp())
    return timestamp_first_day_of_week, timestamp_last_day_of_week


def next_week():
    now = datetime.datetime.now(tz)
    next_week = now + datetime.timedelta(days=7)
    first_day_of_week = next_week - \
        datetime.timedelta(days=(next_week.weekday()+1) % 7)
    last_day_of_week = first_day_of_week + datetime.timedelta(days=6)
    first_day_of_week = tz.localize(first_day_of_week.combine(
        first_day_of_week, datetime.time.min))
    last_day_of_week = tz.localize(last_day_of_week.combine(
        last_day_of_week, datetime.time.max))
    timestamp_first_day_of_week = int(first_day_of_week.timestamp())
    timestamp_last_day_of_week = int(last_day_of_week.timestamp())
    return timestamp_first_day_of_week, timestamp_last_day_of_week


def last_week():
    now = datetime.datetime.now(tz)
    last_week = now - datetime.timedelta(days=7)
    first_day_of_week = last_week - \
        datetime.timedelta(days=(last_week.weekday()+1) % 7)
    last_day_of_week = first_day_of_week + datetime.timedelta(days=6)
    first_day_of_week = tz.localize(first_day_of_week.combine(
        first_day_of_week, datetime.time.min))
    last_day_of_week = tz.localize(last_day_of_week.combine(
        last_day_of_week, datetime.time.max))
    timestamp_first_day_of_week = int(first_day_of_week.timestamp())
    timestamp_last_day_of_week = int(last_day_of_week.timestamp())
    return timestamp_first_day_of_week, timestamp_last_day_of_week


def today():
    now = datetime.datetime.now(tz)
    begining_of_day = tz.localize(now.combine(now, datetime.time.min))
    ending_of_day = tz.localize(now.combine(now, datetime.time.max))
    timestamp_begining_of_day = int(begining_of_day.timestamp())
    timestamp_ending_of_day = int(ending_of_day.timestamp())
    return timestamp_begining_of_day, timestamp_ending_of_day


def tomorrow():
    now = datetime.datetime.now(tz)
    tomorrow = now + datetime.timedelta(days=1)
    begining_of_day = tz.localize(
        tomorrow.combine(tomorrow, datetime.time.min))
    ending_of_day = tz.localize(tomorrow.combine(tomorrow, datetime.time.max))
    timestamp_begining_of_day = int(begining_of_day.timestamp())
    timestamp_ending_of_day = int(ending_of_day.timestamp())
    return timestamp_begining_of_day, timestamp_ending_of_day


def yesterday():
    now = datetime.datetime.now(tz)
    yesterday = now - datetime.timedelta(days=1)
    begining_of_day = tz.localize(
        yesterday.combine(yesterday, datetime.time.min))
    ending_of_day = tz.localize(
        yesterday.combine(yesterday, datetime.time.max))
    timestamp_begining_of_day = int(begining_of_day.timestamp())
    timestamp_ending_of_day = int(ending_of_day.timestamp())
    return timestamp_begining_of_day, timestamp_ending_of_day


def this_month():
    now = datetime.datetime.now(tz)
    first_day_of_month = datetime.date(now.year, now.month, 1)
    last_day_of_month = monthrange(now.year, now.month)[1]
    first_day_of_month = tz.localize(datetime.datetime.combine(
        first_day_of_month, datetime.time.min))
    last_day_of_month = tz.localize(datetime.datetime(
        now.year, now.month, last_day_of_month, 23, 59, 59, 999999))
    timestamp_first_day_of_month = int(first_day_of_month.timestamp())
    timestamp_last_day_of_month = int(last_day_of_month.timestamp())
    return timestamp_first_day_of_month, timestamp_last_day_of_month


def next_month():
    now = datetime.datetime.now(tz)
    next_month = now.replace(
        day=1, month=now.month+1) if now.month != 12 else now.replace(day=1, month=1, year=now.year+1)
    first_day_of_month = datetime.date(next_month.year, next_month.month, 1)
    last_day_of_month = monthrange(
        next_month.year, next_month.month)[1]
    first_day_of_month = tz.localize(datetime.datetime.combine(
        first_day_of_month, datetime.time.min))
    last_day_of_month = tz.localize(datetime.datetime(
        next_month.year, next_month.month, last_day_of_month, 23, 59, 59, 999999))
    timestamp_first_day_of_month = int(first_day_of_month.timestamp())
    timestamp_last_day_of_month = int(last_day_of_month.timestamp())
    return timestamp_first_day_of_month, timestamp_last_day_of_month


def last_month():
    now = datetime.datetime.now(tz)
    last_month = now.replace(
        day=1, month=now.month-1) if now.month != 1 else now.replace(day=1, month=12, year=now.year-1)
    first_day_of_month = datetime.date(last_month.year, last_month.month, 1)
    last_day_of_month = monthrange(
        last_month.year, last_month.month)[1]
    first_day_of_month = tz.localize(datetime.datetime.combine(
        first_day_of_month, datetime.time.min))
    last_day_of_month = tz.localize(datetime.datetime(
        last_month.year, last_month.month, last_day_of_month, 23, 59, 59, 999999))
    timestamp_first_day_of_month = int(first_day_of_month.timestamp())
    timestamp_last_day_of_month = int(last_day_of_month.timestamp())
    return timestamp_first_day_of_month, timestamp_last_day_of_month


def time_range(start, end):
    start_time = datetime.datetime(*start)
    end_time = datetime.datetime(*end)
    begining_of_range = tz.localize(
        start_time.combine(start_time, datetime.time.min))
    ending_of_range = tz.localize(
        end_time.combine(end_time, datetime.time.max))
    timestamp_begining_of_range = int(begining_of_range.timestamp())
    timestamp_ending_of_range = int(ending_of_range.timestamp())
    return timestamp_begining_of_range, timestamp_ending_of_range


def stamp_checker(a: tuple):
    beg = datetime.datetime.fromtimestamp(a[0])
    beg_formated = beg.strftime("%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.fromtimestamp(a[1])
    end_formated = end.strftime("%Y-%m-%d %H:%M:%S")
    return a[0], "is", beg_formated, "-------->", end_formated, a[1]


def print_stamp_checker():
    print("tooooday:", stamp_checker(today()))
    print('tomorrow:', stamp_checker(tomorrow()))
    print("yesterday:", stamp_checker(yesterday()))
    print()
    print("this week:", stamp_checker(this_week()))
    print("next week:", stamp_checker(next_week()))
    print("last week:", stamp_checker(last_week()))
    print()
    print("this month:", stamp_checker(this_month()))
    print("next month:", stamp_checker(next_month()))
    print("last month:", stamp_checker(last_month()))


CONFIGS = getconfigs()
tz = timezone(CONFIGS['times']['tehran.timezone'])
