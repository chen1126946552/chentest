"""date range handle for fetching data from datasource"""

from common.uncategorized.datetime_util import DateTime
from services.common import Fields
from services.exceptions import ServiceError


# pylint: disable=invalid-name,too-many-arguments,too-many-branches


def date_range_convert(timezone, week_start_on, code, value=None, include_today=False):
    """
    date range helper method
    Args:
        timezone (string):
        week_start_on (string): 'monday'|'sunday'
        code(string): e.g. 'last_week'
        value(*): custom value foe special code
        include_today(boolean): if include today in date range

    Returns(tuple(int, int)): (a start timestamp, an end timestamp)

    """
    return DateRange(
        code=code,
        timezone=timezone,
        week_start_on=week_start_on,
        custom_days=value,
        include_today=include_today
    ).compute()


def cwp_date_range_convert(timezone, week_start_on, code, value=None, include_today=False,
                           cwp_code=None, smallest_granularity_in_group_by=None):
    """
    compare with previous date range helper method
    Args:
        timezone (string):
        week_start_on (string): 'monday'|'sunday'
        code(string): e.g. 'last_week'
        value(*): custom value foe special code
        include_today(boolean): if include today in date range
        cwp_code(string): 'pop'|'yoy'|'mom'
        smallest_granularity_in_group_by (string):
        the smallest date granularity appeared in group by fields, e.g 'year', if
        there is no date type field in group by, is None

    Returns(tuple(int, int)): (a start timestamp, an end timestamp)

    """
    assert cwp_code
    return CwpDateRange(
        code=code,
        timezone=timezone,
        week_start_on=week_start_on,
        custom_days=value,
        include_today=include_today,
        cwp_code=cwp_code,
        smallest_granularity_in_group_by=smallest_granularity_in_group_by
    ).compute()


class DateRange:
    """date range helper class"""

    def __init__(self,
                 code,
                 timezone,
                 week_start_on='monday',
                 custom_days='0',
                 include_today=False
                 ):
        """
        Args:
            code (string): date range code e.g. 'last_month', 'this_year'
            timezone (string): e.g. 'Asia/Shanghai'
            week_start_on (string): 'monday'|'sunday'
            custom_days(string): custom values from frontend,
                                e.g. '10' indicates 10 days
                                e.g. '2019/01/01' indicates from 2019-01-01 to now
            include_today(boolean): when date-range is custom period, if include today
        """
        self.code = code
        self.custom_days = custom_days
        self.custom_include_today = include_today
        self.dt = DateTime(tz=timezone, week_start_on=week_start_on)

    def all_time(self):
        """all time"""
        return self.dt.epoch_start.timestamp, self.dt.epoch_end.timestamp

    def past(self):
        """the past * days"""
        days = 0 - int(self.custom_days)
        end = self.dt.today_end if self.custom_include_today else self.dt.today_start
        start = end.offset(day=days)
        return start.timestamp, end.timestamp

    def next(self):
        """the next * days"""
        days = int(self.custom_days)
        start = self.dt.today_start if self.custom_include_today else self.dt.today_end
        end = start.offset(day=days)
        return start.timestamp, end.timestamp

    def today(self):
        """today"""
        start = self.dt.today_start
        end = self.dt.today_end
        return start.timestamp, end.timestamp

    def yesterday(self):
        """yesterday"""
        start = self.dt.today_start.offset(day=-1)
        end = self.dt.today_end.offset(day=-1)
        return start.timestamp, end.timestamp

    def tomorrow(self):
        """tomorrow"""
        start = self.dt.today_start.offset(day=1)
        end = self.dt.today_end.offset(day=1)
        return start.timestamp, end.timestamp

    def this_week(self):
        """this week"""
        start = self.dt.week_start
        end = self.dt.week_end
        return start.timestamp, end.timestamp

    def last_week(self):
        """last week"""
        start = self.dt.week_start.offset(day=-7)
        end = self.dt.week_end.offset(day=-7)
        return start.timestamp, end.timestamp

    def next_week(self):
        """next week"""
        start = self.dt.week_start.offset(day=7)
        end = self.dt.week_end.offset(day=7)
        return start.timestamp, end.timestamp

    def this_month(self):
        """this month"""
        start = self.dt.month_start
        end = self.dt.month_end
        return start.timestamp, end.timestamp

    def last_month(self):
        """last month"""
        start = self.dt.month_start.offset(month=-1).month_start
        end = start.month_end
        return start.timestamp, end.timestamp

    def next_month(self):
        """next month"""
        start = self.dt.month_start.offset(month=1).month_start
        end = start.month_end
        return start.timestamp, end.timestamp

    def this_year(self):
        """this year"""
        start = self.dt.year_start
        end = self.dt.year_end
        return start.timestamp, end.timestamp

    def last_year(self):
        """last year"""
        start = self.dt.year_start.offset(year=-1).year_start
        end = start.year_end
        return start.timestamp, end.timestamp

    def next_year(self):
        """next year"""
        start = self.dt.year_start.offset(year=1).year_start
        end = start.year_end
        return start.timestamp, end.timestamp

    def custom_today(self):
        """custom day to today"""
        start_day = self.custom_days
        start, end = self.dt.get_custom_period(start_day)
        return start.timestamp, end.timestamp

    def custom(self):
        """custom start day to custom end day"""
        start_day, end_day = tuple(sorted(self.custom_days.split('|')))
        start, end = self.dt.get_custom_period(start_day, end_day)
        return start.timestamp, end.timestamp

    def compute(self):
        """
        get the date range tuple
        Returns (tuple(str, str)): start timestamp, end timestamp

        """
        if not hasattr(self, self.code):
            raise ServiceError("Date range code is invalid: %s" % self.code)
        return getattr(self, self.code)()


class CwpDateRange(DateRange):
    """compare with previous  date range helper class"""

    def __init__(self, *args, **kwargs):
        """
        compare with previous
        Args:
            *args: same with super class
            **kwargs:
                cwp_code(string): yoy|pop|mom
                smallest_granularity_in_group_by(string):
                        smallest_granularity_in_group_by (string):
                        the smallest date granularity appeared in group by fields,
                        e.g 'year', None indicates no date fields in group by
        """
        self.cwp_code = kwargs.pop('cwp_code', None)
        if not self.cwp_code:
            raise ServiceError('Invalid compare with previous code: %s' % self.cwp_code)

        self.smallest_granularity_in_group_by = kwargs.pop('smallest_granularity_in_group_by', None)

        super(CwpDateRange, self).__init__(*args, **kwargs)

    def is_no_date_in_group_by(self):
        return not bool(self.smallest_granularity_in_group_by)

    def compute(self):
        """
        get the date range tuple, cwp date range need to be revised according to cwp_code
        Returns (tuple(str, str)): start timestamp, end timestamp

        """
        # the original data req's date range
        start, end = super(CwpDateRange, self).compute()

        # trade-off in milliseconds for those situations that sensitive with midnight boundary
        trade_off = -1

        # WHEN IN DOUBT USE BRUTE FORCE!
        if self.cwp_code == Fields.CompareWithPrevious.YEAR_OVER_YEAR:
            if self.is_no_date_in_group_by() and 'week' in self.code:
                week_number_year = self.dt.replace(ts=start).week_of_year()
                new_start = self.dt.offset(year=-1).nth_week_in_year_start(week_number_year)
                new_end = new_start.new().week_end
            else:
                if 'year' in self.code or \
                        self.smallest_granularity_in_group_by == Fields.Granularity.YEAR:
                    new_start = self.dt.replace(ts=start).offset(year=-1).year_start
                    new_end = self.dt.replace(ts=end + trade_off).offset(year=-1).year_end
                else:
                    new_start = self.dt.replace(ts=start).offset(year=-1)
                    new_end = self.dt.replace(ts=end + trade_off).offset(year=-1,
                                                                         microsecond=trade_off)

        elif self.cwp_code == Fields.CompareWithPrevious.MONTH_OVER_MONTH:
            if self.is_no_date_in_group_by() and 'week' in self.code:
                week_number_month = self.dt.replace(ts=start).week_of_month()
                new_start = self.dt.offset(month=-1).nth_week_in_month_start(week_number_month)
                new_end = new_start.new().week_end
            else:
                if 'month' in self.code or \
                        self.smallest_granularity_in_group_by == Fields.Granularity.MONTH:
                    new_start = self.dt.replace(ts=start).offset(month=-1).month_start
                    new_end = self.dt.replace(ts=end + trade_off).offset(month=-1).month_end
                else:
                    new_start = self.dt.replace(ts=start).offset(month=-1)
                    new_end = self.dt.replace(ts=end + trade_off).offset(month=-1,
                                                                         microsecond=trade_off)

        elif self.cwp_code == Fields.CompareWithPrevious.PERIOD_OVER_PERIOD:
            if 'month' in self.code:  # last|this|next month
                new_start = self.dt.replace(ts=start).offset(month=-1).month_start
                new_end = new_start.month_end
            elif 'year' in self.code:  # last|this|next year
                new_start = self.dt.replace(ts=start).offset(year=-1).year_start
                new_end = new_start.year_end
            else:
                diff = end - start
                new_start = self.dt.new(ts=start - diff)
                new_end = self.dt.new(ts=end - diff)
        else:
            raise ServiceError('Unknown compare with previous code: %s' % self.cwp_code)

        return new_start.timestamp, new_end.timestamp
