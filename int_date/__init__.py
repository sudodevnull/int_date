from datetime import datetime, timedelta, date
import sys

__author__ = 'Cedric Zhuang'
__version__ = '0.1.0'


def _from_str(date_str, format_str=None):
    if format_str is None:
        format_str = "%Y%m%d"
    try:
        ret = datetime.strptime(date_str, format_str).date()
    except ValueError:
        raise ValueError("input is not a valid date: {}".format(date_str))
    return ret


def get_date_from_int(int_date):
    """Convert a ``int`` date to a :class:`datetime` instance

    :param int_date: int number which represents a date
    :return: datetime instance of the date
    """
    date_str = "%s" % int(int_date)
    return _from_str(date_str)


def get_int_day_interval(int_left, int_right):
    """get interval (in day) between two int dates

    :param int_left: first int date
    :param int_right:  second int date
    :return: difference (in day), negative if second date is earlier
             than the first one.
    """
    left_date = get_date_from_int(int_left)
    right_date = get_date_from_int(int_right)
    delta = right_date - left_date
    return delta.days


def get_date_from_diff(i_date, delta_day):
    """calculate new int date with a start date and a diff (in days)

    :param i_date: the starting date
    :param delta_day: diff (in days), negative means past
    :return: result date
    """
    d = get_date_from_int(i_date)
    d += timedelta(delta_day)
    return to_int_date(d)


def to_int_date(the_day):
    """Convert a datetime object or a str/unicode to a int date

    A int str could be one of the following format:
    2015-01-30
    2015/01/30


    :param the_day: datetime,date instance or string
    :exception: ValueError if input could not be converted
    :return: int date
    """
    if sys.version_info >= (3, 0, 0):
        # for Python 3
        if isinstance(the_day, str):
            the_day = _convert_date(the_day)
    else:
        # for Python 2
        if isinstance(the_day, basestring):
            the_day = _convert_date(the_day)

    if isinstance(the_day, datetime) or isinstance(the_day, date):
        ret = the_day.year * 10000 + the_day.month * 100 + the_day.day
    else:
        raise ValueError("input should be a datetime/"
                         "date/str/unicode instance.")
    return ret


def today():
    """Get the today of int date

    :return: int date of today
    """
    the_day = date.today()
    return to_int_date(the_day)


def _convert_date(date_str):
    """convert a *date_str* to int date

    convert string '2015-01-30' to int 20150130
    convert string '2015/01/30' to int 20150130
    :return: int format of date
    """
    ret = None

    if '-' in date_str:
        ret = _from_str(date_str, "%Y-%m-%d")
    elif '/' in date_str:
        ret = _from_str(date_str, "%Y/%m/%d")
    return ret


def in_year(day, years):
    """check if day is in years list or year

    :param day: date
    :param years: list of years or year
    :return: true if in, otherwise false
    """
    year = int(day / 1e4)
    return _in_range_or_equal(year, years)


def in_month(day, months):
    """check if day is in months list or month

    :param day: date
    :param months: list of months or month
    :return: true if in, otherwise false
    """
    month = int(day % 10000 / 100)
    return _in_range_or_equal(month, months)


def in_date(day, dates):
    """check if day is in dates list or date

    :param day: date
    :param dates: list of dates or date
    :return: true if in, otherwise false
    """
    the_date = int(day % 100)
    return _in_range_or_equal(the_date, dates)


def _in_range_or_equal(value, to_compare):
    if hasattr(to_compare, '__iter__'):
        ret = value in to_compare
    else:
        ret = value == to_compare
    return ret
