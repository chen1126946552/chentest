"""util class/method about date&time"""
import logging
import datetime
from math import ceil
from dateutil import relativedelta
import pytz

# pylint: disable=missing-docstring,invalid-name,too-many-arguments,too-many-public-methods

logger = logging.getLogger(__name__)


class DateTime:
    # pylint: disable=too-many-arguments
    def __init__(self, tz=None, dt=None, ts=None, ds=None, fmt="%Y-%m-%d %H:%M:%S",
                 week_start_on='monday'):
        """
        An DateTime object can initialized with either a
        python datetime.datetime object or a timestamp
        Args:
            tz(string): timezone
            dt(datetime.datetime object): a datetime.datetime object (default is utc now)
            ts(int): a timestamp
            week_start_on(string): monday or sunday
        """

        self.timestamp_offset = 0
        self._week_start_on = self._custom_week_start_init(week_start_on)
        self._fmt = fmt

        # initialize timezone and datetime, order can not be changed
        self._tz = self._timezone_init(tz)
        self._datetime_obj = self._datetime_init(dt, ts, ds, fmt)

    def __str__(self):
        return self._datetime_obj.strftime("%Y-%m-%dT%H:%M:%S")

    def _timezone_init(self, tz):
        """tz initial helper method"""
        if tz:
            if isinstance(tz, pytz.BaseTzInfo):
                timezone = tz
            elif isinstance(tz, str):
                try:
                    timezone = pytz.timezone(tz)
                except pytz.exceptions.UnknownTimeZoneError:
                    logger.error("Unknown Timezone: %s", tz)
                    timezone = pytz.utc
            else:
                timezone = tz
        else:
            timezone = pytz.utc
        return timezone

    def _datetime_init(self, dt, ts, ds, fmt="%Y-%m-%d %H:%M:%S"):
        """datetime initial helper method"""
        if dt:
            assert isinstance(dt, datetime.datetime), \
                'Argument dt must be a datetime object'
            self._tz = dt.tzinfo or pytz.utc
            return dt
        if ts:
            assert isinstance(ts, int), \
                'Argument ts must be an integer'
            if len(str(ts)) > 10:
                self.timestamp_offset = int(str(ts)[10:])
                ts = int(str(ts)[:10])
            return datetime.datetime.fromtimestamp(ts, tz=self._tz)
        if ds:
            if 'T' in ds:
                return datetime.datetime.strptime(ds, fmt)
            ts = datetime.datetime.strptime(ds, fmt).replace(
                tzinfo=pytz.UTC).timestamp() - self.get_offset(self._tz.zone)
            return datetime.datetime.fromtimestamp(ts, tz=self._tz)
        return datetime.datetime.now(tz=self._tz)

    def _custom_week_start_init(self, week_start_on):
        """custom week start day initial helper method"""
        if week_start_on:
            # Monday starts a week, *International Practice
            assert week_start_on in ['monday', 'sunday'], \
                'Week start day must be monday or sunday.'
        else:
            week_start_on = 'monday'
        return week_start_on

    # pylint: disable=too-many-arguments
    def offset(self, year=0, month=0, day=0, hour=0, minute=0, second=0, microsecond=0):
        """
        Datetime backed(negative) or headed(positive) for given time
        Args:
            year(int): years offset
            month(int): months offset
            day(int): days offset
            hour(int): hours offset
            minute(int): minutes offset
            second(int): seconds offset
            microsecond(int): microseconds offset
        Returns:
            a new DataTime object that has backed or headed for given time
        """
        dt = self._datetime_obj + \
             relativedelta.relativedelta(
                 years=year,
                 months=month,
                 days=day,
                 hours=hour,
                 minutes=minute,
                 seconds=second,
                 microseconds=microsecond
             )
        return self.new(dt=dt)

    def new(self, dt=None, ts=None):
        if not (dt or ts):
            dt = self._datetime_obj
        return DateTime(
            dt=dt,
            ts=ts,
            tz=self._tz,
            week_start_on=self._week_start_on
        )

    def replace(self, dt=None, ts=None, tz=None, ds=None, fmt=None, week_start_on=None):
        """change the attribute of current object"""
        if tz:
            self._tz = self._timezone_init(tz)
        if dt or ts or (ds and fmt):
            self._datetime_obj = self._datetime_init(dt, ts, ds, fmt)
        if week_start_on:
            self._custom_week_start_init(week_start_on)
        return self

    @property
    def datetime(self):
        """to datetime object"""
        return self._datetime_obj

    @property
    def timestamp(self):
        """to timestamp(milliseconds)"""
        return int(self._datetime_obj.timestamp() * 1000) + self.timestamp_offset

    @property
    def format_str(self):
        """to format string"""
        return self._datetime_obj.strftime(self._fmt)

    def format(self, fmt):
        return self._datetime_obj.strftime(fmt)

    @property
    def epoch_start(self):
        """UNIX Epoch time's start"""
        return self.new(dt=datetime.datetime(1970, 1, 1, tzinfo=pytz.utc))

    @property
    def epoch_end(self):
        """UNIX Epoch time's end for our service"""
        return self.new(dt=datetime.datetime(2286, 11, 21, tzinfo=pytz.utc))

    @property
    def today_start(self):
        """today start"""
        dt = self._datetime_obj.replace(
            hour=0, minute=0, second=0, microsecond=0)
        return self.new(dt=dt)

    @property
    def today_end(self):
        """today end"""
        dt = self.today_start.datetime + datetime.timedelta(days=1)
        return self.new(dt=dt)

    @property
    def week_start(self):
        """this week start"""
        days = self._datetime_obj.weekday() if self._week_start_on == 'monday' \
            else (self._datetime_obj.isoweekday() % 7)
        dt = (self._datetime_obj - datetime.timedelta(days=days)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return self.new(dt=dt)

    @property
    def week_end(self):
        """this week end"""
        dt = self.week_start.datetime + datetime.timedelta(days=7)
        return self.new(dt=dt)

    def nth_week_in_year_start(self, n):
        """the start day of nth week in year"""
        if n <= 1:
            return self.year_start
        first_day = self.year_start.offset(day=(n - 1) * 7)
        return first_day.week_start

    def nth_week_in_month_start(self, n):
        """the start day of nth week in month"""
        if n <= 1:
            return self.month_start
        first_day = self.month_start.offset(day=(n - 1) * 7)
        return first_day.week_start

    def week_of_month(self):
        """ Returns the week number of the month"""
        first_day = self._datetime_obj.replace(day=1)
        dom = self._datetime_obj.day
        week_days = first_day.weekday() if \
            self._week_start_on == 'monday' else first_day.isoweekday() % 7
        adjusted_dom = dom + week_days
        return int(ceil(adjusted_dom / 7.0))

    def week_of_year(self):
        """ Returns the week number of the year"""
        return int(self._datetime_obj.isocalendar()[1])

    @property
    def month_start(self):
        """this month start"""
        dt = self._datetime_obj.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.new(dt=dt)

    @property
    def month_end(self):
        """this month end"""
        dt = self.month_start.datetime + relativedelta.relativedelta(months=1)
        return self.new(dt=dt)

    @property
    def year_start(self):
        """this year start"""
        dt = self._datetime_obj.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return self.new(dt=dt)

    @property
    def year_end(self):
        """this year end"""
        dt = self.year_start.datetime + relativedelta.relativedelta(years=1)
        return self.new(dt=dt)

    def get_custom_period(self, start_str, end_str=None, fm='%Y/%m/%d'):
        """custom period, default end is today(now)"""

        if end_str and start_str > end_str:
            start_str, end_str = end_str, start_str
        start = self._tz.localize(datetime.datetime.strptime(start_str, fm))
        end = self._tz.localize(datetime.datetime.strptime(end_str, fm)) \
            if end_str else self.today_start.datetime
        # from start day start to end day end
        return self.new(dt=start), self.new(dt=end).offset(day=1)

    @staticmethod
    def get_offset(tz_name):
        """
        get offset to utc by timezone info
        Args:
            tz_name(string): timezone
        Returns(int): offset in seconds

        """
        if not isinstance(tz_name, str):
            return 0
        try:
            return int(datetime.datetime.now(pytz.timezone(tz_name)).utcoffset().total_seconds())
        except pytz.exceptions.UnknownTimeZoneError:
            logger.warning("Unknown Timezone: %s", tz_name)
            return 0

    @staticmethod
    def timestamp_to_date_string(ts, fm='%Y-%m-%d %H:%M:%S', tz_offset=0):
        """transmit a timestamp(milliseconds) to a datetime string in a fix format"""
        ts = str(ts)
        if len(ts) > 10:
            ts = ts[:10]
        return datetime.datetime.utcfromtimestamp(int(ts) + tz_offset).strftime(fm)
