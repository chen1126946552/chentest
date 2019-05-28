"""compare with previous period data handling"""
import logging
from copy import deepcopy
import pandas as pd
from common.uncategorized.datetime_util import DateTime
from services.exceptions import ServiceError
from services.common import Fields, Constant

# pylint: disable=invalid-name,too-many-arguments

logger = logging.getLogger(__name__)


class CwpDimensionCompare:
    """compare constants"""
    EQUAL = 0
    LARGER = 1
    SMALLER = -1


# pylint: disable=too-many-instance-attributes
class CompareWithPreviousHandler:
    """compare with previous handler"""

    def __init__(self, df1, df2, fields, setting, sort=False,
                 timezone=None, week_start_on=None):
        """
        Args:
            df1(pd.DataFrame): original data frame
            df2(pd.DataFrame): the second time(cwp) data frame
            fields(list): req fields
            setting(dict): cwp settings
            sort(dict): req sort field
            timezone(string): timezone name
            week_start_on(string): monday|sunday
        """
        self.df1 = df1
        self.df2 = df2
        self.fields = fields
        self.setting = setting
        self.tz = timezone
        self.ws = week_start_on
        self.sort = sort

    def get_new_cols(self):
        """make the new column-headers for data frame, as cwp need setting new columns in df"""
        sorted_fields = _sorted_fields_as_dimension_first(self.fields)
        cwps = [f['uuid'] for f in self.setting['fields']]
        new_cols = []
        for field in sorted_fields:
            new_cols.append(field['uuid'])
            if field['uuid'] in cwps:
                new_cols.append(field['uuid'] + ':cwp')
        return new_cols

    def execute(self):
        """cwp handler trigger"""
        new_cols = self.get_new_cols()
        if self.df1.empty:
            return pd.DataFrame(data=[], columns=new_cols, dtype=object)

        rows = self.df1.where(self.df1.notnull(), None).values.tolist()
        cwp_rows = self.df2.where(self.df2.notnull(), None).values.tolist()
        data = cwp_data_merge(
            rows,
            cwp_rows,
            self.fields,
            self.setting,
            self.sort,
            tz=self.tz,
            ws=self.ws
        )
        return pd.DataFrame(data=data, columns=new_cols, dtype=object)


def cmp(val1, val2):
    """compare two values"""

    if val1 == val2:
        return CwpDimensionCompare.EQUAL
    elif val1 < val2:
        return CwpDimensionCompare.SMALLER
    else:
        return CwpDimensionCompare.LARGER


def _find_th_week(dt):
    """get the week's number of that year"""
    return dt.datetime.isocalendar()[1]


def _last_year(dt):
    """get the same moment of last year"""
    return dt.offset(year=-1).timestamp


def _last_month(dt):
    """get the same moment of last month"""
    return dt.offset(month=-1).timestamp


def _last_period(dt, time_diff_microseconds):
    """get the same moment before time_diff_microseconds"""
    return dt.timestamp - int(time_diff_microseconds or 0)


def _compute_time(dt, code, custom_period):
    """
    compute time depending on the cwp code
    Args:
        dt (common.Datetime): custom datetime object
        code (string): pop|yoy|mom
        custom_period (int): if pop is set, custom_period is the time diff in microseconds
    Returns: (string) timestamp

    """
    if code == Fields.CompareWithPrevious.PERIOD_OVER_PERIOD:
        return _last_period(dt, time_diff_microseconds=custom_period)
    if code == Fields.CompareWithPrevious.YEAR_OVER_YEAR:
        return _last_year(dt)
    if code == Fields.CompareWithPrevious.MONTH_OVER_MONTH:
        return _last_month(dt)
    raise ServiceError('Invalid compare with previous period code: %s' % code)


def _cwp_datetime_compare(ts1, ts2, code, custom_period, granularity=None, tz=None, ws=None):
    """
    check if two timestamp matches, match means ts2 is ts1
    Args:
        ts1 (int): timestamp 1
        ts2 (int): timestamp 2
        code: yoy|mom|pop
        custom_period: if pop is set, time diff in microseconds
        granularity:
            special case, if granularity is 'Week', need special handle
        tz(string): timezone e.g 'Asia/Shanghai'
        ws(string): week start on 'monday' | 'sunday'
    Returns:

    """
    # if granularity is 'Week', t1 matches t2 means t1 and t2 have
    # the same week number in their years respectively
    dt1 = DateTime(tz=tz, week_start_on=ws, ts=ts1)
    dt2 = DateTime(tz=tz, week_start_on=ws, ts=ts2)
    if granularity == Fields.Granularity.WEEK:
        return cmp(_find_th_week(dt1), _find_th_week(dt2))
    return cmp(_compute_time(dt1, code, custom_period=custom_period), ts2)


def _cwp_compute_fields_idx(original_fields, cwp_fields):
    """find all cwp fields original indexes in the original field list"""
    result_list = []
    for idx, o_field in enumerate(original_fields):
        for c_field in cwp_fields:
            if c_field['uuid'] == o_field['uuid']:
                result_list.append(idx)
    return result_list


def _sorted_fields_as_dimension_first(fields):
    """put all dimension fields before metrics, stable sorting"""
    return sorted(fields, key=lambda f: int(f.get('groupBy') is True), reverse=True)


def _is_metrics_comes_before_dimensions(original_fields):
    """check if there is metric field in front of dimension field"""
    fields_sorted = _sorted_fields_as_dimension_first(original_fields)
    return any(fields_sorted[idx]['id'] != original_fields[idx]['id'] for idx in
               range(len(original_fields)))


def _reorganize_on_data_rows(rows, seq_before, seq_after):
    """
    reorganize data rows to new sequence
    Args:
        rows(list): 2-dimension-arrays
        seq_before(list): a list indicates original seq e.g. ['a', 'b', 'c']
        seq_after(list): a list indicates after reorganized seq e.g. ['c', 'b', 'a']
    Returns(list):
        new list reorganized with the new sequence
    """
    return pd.DataFrame(rows, columns=seq_before, dtype=object).reindex(
        columns=seq_after).values.tolist()


def _cwp_compute_dimension_count(fields):
    """compute the dimension fields number"""
    return len(list(filter(lambda f: f.get('groupBy'), fields)))


def _get_sort_by_field_idx(sort_by, fields):
    """
    Returns (int): sorting field idx
    """
    for idx, field in enumerate(fields):
        if field['id'] == sort_by['field']['id']:
            return idx
    raise ServiceError("Can not match sorting field, fieldId: %s" % sort_by['field']['id'])


# pylint: disable=too-many-locals,too-many-statements
def cwp_data_merge(rows, cwp_rows, fields, cwp_settings, sort_by, tz=None, ws=None):
    """
    Args:
        rows (list): (2-dimension-list): data lists
        cwp_rows(list): (2-dimension-list): data lists
        fields (list): original fields (containing dimensions and metrics)
        cwp_settings (dict): cwp related params
                -- code (string): yoy|mom|pop
                -- fields (list): cwp fields list(only metrics)
                -- compute (string): growth_rate| growth
                -- period: if pop is set, time diff in microseconds
        sort_by (dict): sort_by info
                -- fieldId(string): sorting field id
                -- order (string): 'desc' or 'asc'
        tz (string): timezone name
        ws (string): week start day 'monday'|'sunday'
    Returns:
        the total result integrated both original data and cwp data
    """

    # data rows / header / fields
    fields = deepcopy(fields)
    # cwp setting fields
    cwp_code = cwp_settings['code']
    cwp_fields = cwp_settings['fields']
    cwp_compute = cwp_settings['computing']
    cwp_period_microseconds = cwp_settings.get('custom_period')

    # check if the fields' sequence is that dimensions in fields always come before metrics
    # if not, then we need reorganize fields and two data result to `dims then metrics`
    # sequence to make merging data easily
    is_data_rows_need_reorganize = _is_metrics_comes_before_dimensions(fields)
    if is_data_rows_need_reorganize:
        seq_before = [f['uuid'] for f in fields]
        fields = _sorted_fields_as_dimension_first(fields)
        seq_after = [f['uuid'] for f in fields]
        rows = _reorganize_on_data_rows(rows, seq_before, seq_after)
        cwp_rows = _reorganize_on_data_rows(cwp_rows, seq_before, seq_after)

    # the dimension fields number in original fields
    # will help the manipulate the merged work when slicing rows
    # * dimension fields always comes first then metric fields
    dm_cnt = _cwp_compute_dimension_count(fields)

    # the list which shows the cwp fields positions in fields list
    # e.g.
    # original fields: ['d1', 'd2', 'm1', 'm2', 'm3']
    # cwp fields are 'm1', 'm3'
    # then idx list is [2, 4]
    cwp_fields_idx_list = _cwp_compute_fields_idx(fields, cwp_fields)

    # the list which shows the cwp fields positions after merged in fields list
    # e.g
    # in above example, final row is ['d1', 'd2', 'm1', '*m1*', 'm2', 'm3', '*m3*']
    # so post_idx_list is [3, 6]
    cwp_fields_idx_list_after_merged = \
        [idx + pos + 1 for pos, idx in enumerate(cwp_fields_idx_list)]

    # e.g. in above example, if sortBy field is 'm2', then its idx is 3
    # its after merged idx is 4
    if sort_by:
        sort_by_idx = _get_sort_by_field_idx(sort_by, fields)
        sort_by_idx_after_merged = \
            sort_by_idx + len(list(filter(lambda x: x < sort_by_idx, cwp_fields_idx_list)))
        reverse = sort_by['order'] == 'desc'
    else:
        # if there is no sort_by settings, resort the data rows on the first column by default
        sort_by_idx, sort_by_idx_after_merged, reverse = 0, 0, False

    # Check if the data rows need to be resorting in order
    # to improve the efficiency of data merging process.
    # If the data result has already sorted by its only dimension field,
    # then we can merge the two data rows in O(n) + 2*nlog(n)
    is_data_rows_need_resort = not (fields[sort_by_idx].get('groupBy') and dm_cnt == 1)

    # after merged, the length of one row in data
    total_row_length = len(rows[0]) + len(cwp_fields_idx_list)

    if is_data_rows_need_resort:
        # resorting the two data rows on its dimension fields
        # the last row is summary, no need resorting
        rows = sorted(
            rows[:-1], key=lambda item: tuple(
                item[_] if item[_] is not None else float('-inf') for _ in range(dm_cnt))
        ) + [rows[-1]] if rows else []
        cwp_rows = sorted(
            cwp_rows[:-1], key=lambda item: tuple(
                item[_] if item[_] is not None else float('-inf') for _ in range(dm_cnt))
        ) + [cwp_rows[-1]] if cwp_rows else []

    logger.debug(rows)
    logger.debug(cwp_rows)

    def _secondary_compute(o_row, c_row):
        """
        helper method the process some secondary computing
        Args:
            o_row: the original row e.g. ['d1', 'd2', 'm1', 'm2', 'm3']
            c_row: the cwp row e.g. ['d1', 'd2', '*m1*', '_', '*m3*']
        Returns:
            a new c_row after secondary computing on '*m1*' and '*m3*'
            [d1, d2, m1c, _, m3c]
        """

        def gr(cur, last):
            # growth
            try:
                return cur - last
            except Exception:  # pylint: disable=broad-except
                return None

        def grr(cur, last):
            # growth-rate
            try:
                return round(float(cur - last) / last, Constant.Data.COMPUTING_PRECISION)
            except Exception:  # pylint: disable=broad-except
                return None

        if cwp_compute == 'growth':
            compute_func = gr
        elif cwp_compute == 'growth_rate':
            compute_func = grr
        else:
            compute_func = lambda cur, last: last

        new_c_row = c_row[:]
        for i in cwp_fields_idx_list:
            new_c_row[i] = compute_func(o_row[i], c_row[i])
        return new_c_row
        #
        # c_dimensions, c_metrics = c_row[:dm_cnt], c_row[dm_cnt:]
        # # i is the c_row's index, from 0 --> end
        # # j is the index of cwp field's indexs, in this e.g [3, 6]
        # for i, j in enumerate(cwp_fields_idx_list):
        #     c_dimensions.append(compute_func(o_row[j], c_metrics[i]))
        # return c_dimensions

    def _one_row_merge(o_row, c_row):
        """
        helper method to merged one row in data
        Args:
            o_row (list): the original row e.g. ['d1', 'd2', 'm1', 'm2', 'm3']
            c_row (list or None): the cwp row
            e.g. ['d1', 'd2', '*m1*', '*m3*'] or None (can not find the matched row)
        Returns (list):
            a merged row e.g. ['d1', 'd2', 'm1', '*m1*', 'm2', 'm3', '*m3*']

        """

        # computing for secondary computing setting
        # if c_row is None, which indicates not matched c_row found,
        if cwp_compute and c_row:
            c_row = _secondary_compute(o_row, c_row)

        # row initialization
        new_row = [None for _ in range(total_row_length)]

        # two indexes recording each step for o elements and c elements
        o_idx, c_idx = 0, 0
        for i in range(total_row_length):
            if i in cwp_fields_idx_list_after_merged:
                if c_row:
                    new_row[i] = c_row[cwp_fields_idx_list[c_idx]]
                    c_idx += 1
                else:
                    continue
            else:
                new_row[i] = o_row[o_idx]
                o_idx += 1
        return new_row

    def _rows_compare(o_row, c_row):

        if not o_row or not c_row:
            return CwpDimensionCompare.EQUAL

        # if all the dimension values are None, not matches, let compare rows move
        # the summary row is a special case which meets such situation
        if all([o is None for o in o_row]) or all([c is None for c in c_row]):
            return CwpDimensionCompare.LARGER

        for idx, _ in enumerate(o_row):
            result = _dimension_values_compare(o_row[idx], c_row[idx], idx=idx)
            if not result == CwpDimensionCompare.EQUAL:
                return result
        return CwpDimensionCompare.EQUAL

    def _dimension_values_compare(val1, val2, idx):
        if val1 is None and val2 is None:
            return CwpDimensionCompare.EQUAL
        if fields[idx].get('type') == 'date':
            return _cwp_datetime_compare(val1, val2, cwp_code, cwp_period_microseconds,
                                         granularity=fields[idx].get('granularity'),
                                         tz=tz,
                                         ws=ws)
        return cmp(val1, val2)

    def _data_merge():
        """
        the main process doing merge for two data rows
        """
        merged_rows = []
        # original data rows and cwp data rows all in same order
        # traversing one time original rows, for each row, find the matched
        # row in cwp data rows(traversing cwp rows from last matched point),
        # if not match, fill in default values.
        # if match, merge them and continue traversing original rows.
        rows_idx, c_rows_idx = 0, 0

        while rows_idx < len(rows) and c_rows_idx < len(cwp_rows):
            r = rows[rows_idx]
            c = cwp_rows[c_rows_idx]

            compare_result = _rows_compare(r[:dm_cnt], c[:dm_cnt])
            if compare_result == CwpDimensionCompare.EQUAL:
                merged_rows.append(_one_row_merge(r, c))
                rows_idx += 1
                c_rows_idx += 1
            else:
                if compare_result < CwpDimensionCompare.EQUAL:
                    merged_rows.append(_one_row_merge(r, None))
                    rows_idx += 1
                else:
                    c_rows_idx += 1

        if rows_idx == len(rows):
            pass
        elif c_rows_idx == len(cwp_rows):
            while rows_idx < len(rows):
                merged_rows.append(_one_row_merge(rows[rows_idx], None))
                rows_idx += 1
        return merged_rows

    data_merged = _data_merge()

    if is_data_rows_need_resort:
        # resorting data rows back to the original/default order
        data_merged = sorted(data_merged[:-1],
                             key=lambda item: item[sort_by_idx_after_merged] if
                             item[sort_by_idx_after_merged] is not None else float('-inf'),
                             reverse=reverse) + [data_merged[-1]]

    return data_merged
