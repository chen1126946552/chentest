"""For data fetching and data result computing"""

from __future__ import absolute_import

import logging
from copy import deepcopy
from functools import reduce
from dataclasses import asdict
import pandas as pd
from common.uncategorized.datetime_util import DateTime
from common.http.utils import post_json
from services.downstream import make_ds_call_url
from services.common import Fields
from .metadata import ParsedParams, ParsedReqBody
from .date_range import date_range_convert, cwp_date_range_convert
from .calculate import CalculatedDataHandler
from .aggregate import AggregateHandler
from .analyze import AnalyzeDataHandler
from .compare_with_previous import CompareWithPreviousHandler

# pylint: disable=invalid-name

logger = logging.getLogger(__name__)


def get_data_raw(ds_code, req_body):
    """helper method to directly get data back from data source"""
    url = make_ds_call_url(ds_code, '/data')
    logger.debug("Request to datasource: %s", req_body)
    data_raw = post_json(url, body=req_body)
    logger.debug("Response from datasource: %s", data_raw)
    return data_raw


def get_data(ds_code, req_body):
    """fetching data entry, api called by external """
    return FetchingDataHandler(ds_code, req_body).get_result()


# pylint: disable=not-an-iterable,too-many-public-methods,no-member
class FetchingDataHandler:
    """Handler for fetching data back from datasources"""

    def __init__(self, ds_code, params):
        """
        Args:
            ds_code(string): data-source code
            params(dict): raw data params
        """
        self.ds_code = ds_code
        self.params = ParsedParams(**params)
        self.group_by_columns = self.get_groupby_columns()
        self.include_summary = True
        self.resort = False
        self.cwp_date_range = None
        self.req_body = self.make_req_body()

    @property
    def is_cal_active(self):
        """check if contains calculated fields in current data fetching request"""
        return bool(self.params.calculatedFields)

    @property
    def is_cwp_active(self):
        """check if contains compare with previous fields in current data fetching request"""
        return bool(self.params.compareWithPrevious)

    def get_ds_config(self):
        """gets datasource config info"""
        return self.params.dsInfo.get('config', {})

    @property
    def is_provide_raw_data(self):
        """
        Indicates if the datasource provides raw data without any aggregation or sorting.
         If set to true,the framework handles sorting and aggregation; otherwise it's
         datasource service's responsibility to return already sorted and aggregated data.
        """
        return bool(self.get_ds_config().get('data', {}).get('provideRawData'))

    def make_req_body(self):
        """make req body to sending to downstream (datasource service layer)"""
        parsed = ParsedReqBody()
        parsed.token = self.parse_token()
        parsed.path = self.parse_path()
        parsed.locale = self.parse_locale()
        parsed.timezoneOffset = self.parse_timezone_offset()
        parsed.paging = self.parse_paging()
        parsed.filters = self.parse_filters()
        parsed.dateRange = self.parse_date_range()
        parsed.sort = self.parse_sort()
        parsed.segment = self.parse_segment()
        parsed.fields = self.parse_fields()
        return parsed

    def get_groupby_columns(self):
        """compute number of dimension(group by) fields"""
        return [f['uuid'] for f in self.params.fields if f.get('groupBy')]

    def parse_token(self):
        return deepcopy(self.params.token)

    def parse_path(self):
        return deepcopy(self.params.path)

    def parse_locale(self):
        return self.params.locale

    def parse_timezone_offset(self):
        """parse timezoneOffset field in req body"""
        return DateTime.get_offset(self.params.timezone)

    def parse_paging(self):
        """parse page(records per page limit) field in req body"""
        return deepcopy(self.params.paging)

    def parse_filters(self):
        """parse filters in req body"""
        filters = self.params.filters
        new_filters = []
        dt_helper = DateTime(tz=self.params.timezone, week_start_on=self.params.weekStartOn)
        for fil in filters:
            new_fil = {"fieldId": fil['field']['id'], "operator": fil['operator']}
            values = fil['values']
            if fil['field']['type'] == 'date':
                fmt = fil['field']['dataFormat']
                assert fmt is not None
                values = [dt_helper.replace(ds=val, fmt=fmt).timestamp for val in fil['values']]
            new_fil['values'] = values
            new_filters.append(new_fil)
        return new_filters

    def parse_date_range(self):
        """parse dateRange in req body"""
        if self.params.dateRange:
            start, end = date_range_convert(
                self.params.timezone,
                self.params.weekStartOn,
                self.params.dateRange['code'],
                self.params.dateRange.get('value'),
                self.params.dateRange.get('isIncludeToday')
            )
            return {
                'field': self.params.dateRange.get('field'),
                'start': start,
                'end': end
            }
        return {}

    def parse_date_range_cwp(self):
        """parse dateRange in req body for the second time request
        in compare with previous situation
        """
        if self.params.dateRange:
            start, end = cwp_date_range_convert(
                self.params.timezone,
                self.params.weekStartOn,
                self.params.dateRange['code'],
                self.params.dateRange.get('value'),
                self.params.dateRange.get('isIncludeToday'),
                self.params.compareWithPrevious['code'],
                self._group_by_smallest_granularity()
            )
            return {
                'field': self.params.dateRange.get('field'),
                'start': start,
                'end': end
            }
        return {}

    def parse_sort(self):
        """parse sorting in req body, if the sort field in req params
            is not the ds native field, set sort to None,
            do the sorting work here when data getting back"""
        if self.params.sort:
            for f in self.params.fields:
                if self.params.sort.get('field', {}).get('id') == f['id']:
                    return deepcopy(self.params.sort)
            self.resort = True
        return {}

    def parse_segment(self):
        """parse segment in req body"""
        return deepcopy(self.params.segment)

    def parse_fields(self):
        """parse fields in req body
            if contains calculated fields, need fill the hidden fields in req body
        """
        raw_fields = deepcopy(self.params.fields)
        raw_ids = set(rf['id'] for rf in raw_fields)
        if self.is_cal_active:
            candidate_fields = reduce(lambda i, j: i + j,
                                      [calf['fields'] for calf in self.params.calculatedFields])
            for idx, cf in enumerate(candidate_fields):
                if cf['id'] not in raw_ids:
                    cf['uuid'] = f'hidden_field:{idx}'
                    raw_fields.append(cf)
        return raw_fields

    def parse_calculated_fields(self):
        """ datasource native cal fields not handle yet"""
        raise NotImplementedError('datasource-supported calculated fields is not handled yet.')

    def _group_by_smallest_granularity(self):
        """find the smallest date granularity in group by fields"""
        sorted_fields_on_granularity = \
            sorted([f for f in self.req_body.fields if f.get('groupBy')],
                   key=lambda f: Fields.Granularity.granularity_order_map[f.get('dataFormat')])
        return sorted_fields_on_granularity[0].get(
            'dataFormat') if sorted_fields_on_granularity else None

    def do_aggregate_calc(self, data_raw):
        """
        If the data source returns detailed data, the DM performs the aggregation calculation
        """
        cols = [f['uuid'] for f in self.req_body.fields]
        df = pd.DataFrame(data=data_raw['data'], columns=cols)
        result = AggregateHandler(df, self.req_body).execute()
        return result

    def do_calculate(self, data_frame, inplace=True):
        """
        computing the calculated fields columns *in place* (actually adding new columns)
        Args:
            data_frame(pd.DataFrame): the last step processed data frame
            inplace(boolean): if modify the data frame inplace,
            if not a modified original data frame's swallow copy will return
        Returns: no-return

        """
        result_df = CalculatedDataHandler(data_frame,
                                          self.req_body.fields,
                                          self.params.calculatedFields
                                          ).execute(inplace=inplace)
        return result_df

    def do_analyze(self, data_frame, inplace=True):
        """
        computing the analysis fields columns *in place*
        Args:
            data_frame(pd.DataFrame): the last step processed data frame
            inplace(boolean): if modify the data frame inplace,
            if not a modified original data frame's swallow copy will return
        Returns(pd.DataFrame): processed data frame

        """
        ana_op_map = {f['uuid']: f['anal'] for f in
                      self.params.fields + self.params.calculatedFields if f.get('anal')}

        df_columns = list(data_frame)
        for df_col in df_columns:
            if df_col.endswith(':cwp'):
                original_uuid = df_col[:-4]
                if original_uuid in ana_op_map:
                    ana_op_map[df_col] = ana_op_map[original_uuid]

        result_df = AnalyzeDataHandler(data_frame,
                                       ana_op_map,
                                       self.group_by_columns
                                       ).execute(inplace=inplace)
        return result_df

    def do_compare_with_previous(self, data_frame_1, data_frame_2):
        """
        computing the compare with previous fields columns
        Args:
            data_frame_1(pd.DataFrame): the first time df getting back
            data_frame_2(pd.DataFrame): the second time(cwp) df getting back
        Returns(pd.DataFrame):
                a new df object containing cwp fields
        """
        total_fields = self.req_body.fields + self.params.calculatedFields
        cwp_setting = self.params.compareWithPrevious
        date_range = self.req_body.dateRange
        if cwp_setting.get('code') == Fields.CompareWithPrevious.PERIOD_OVER_PERIOD:
            cwp_setting['custom_period'] = date_range['end'] - date_range['start']
        result_df = CompareWithPreviousHandler(data_frame_1,
                                               data_frame_2,
                                               total_fields,
                                               cwp_setting,
                                               self.req_body.sort,
                                               self.params.timezone,
                                               self.params.weekStartOn).execute()
        return result_df

    def execute(self, cwp_req=False):
        """
        Fetching data back and computing
        If the original req params contain compare with previous fields

        Args:
            cwp_req(boolean):
                if true, indicates this time executing is for compare with previous data
                need do some work on modifying req body, e.g. a new date range
        Returns (pd.DataFrame):
            a df object encapsulating the data result in it
            - calculated fields is handled here
            - analysis fields is handled here
        """
        if cwp_req:
            self.req_body.dateRange = self.parse_date_range_cwp()

        data_raw = get_data_raw(self.ds_code, asdict(self.req_body))

        if self.is_provide_raw_data:
            data_raw = self.do_aggregate_calc(data_raw)

        data = data_raw['data']
        summary = data_raw.get('summaryValues')

        if summary:
            data.append(self._summary_row_filled(summary, self.req_body.fields))
        else:
            if not cwp_req:
                self.include_summary = False

        cols = [f['uuid'] for f in self.req_body.fields]
        df = pd.DataFrame(data=data, columns=cols, dtype=object)

        if self.is_cal_active:
            df = self.do_calculate(df)

        if not df.empty and self.is_cwp_active and not cwp_req:
            self.cwp_date_range = self.req_body.dateRange
            df_cwp = self.execute(cwp_req=True)
            df = self.do_compare_with_previous(df, df_cwp)
        return df

    @classmethod
    def _summary_row_filled(cls, summary_row, fields):
        """
        To make secondary computing easy, decorated summary
        row(fill none for dimensions) to fit the data rows's structure
        Args:
            summary_row(list): summary values list return by datasource
            fields(list): current req fields
        Returns (list): a filled row (None at dimensions' positions)

        """
        metrics_idx, filled = 0, []
        for fil in fields:
            if fil.get('groupBy'):
                filled.append(None)
            else:
                filled.append(summary_row[metrics_idx])
                metrics_idx += 1
        return filled

    def post_reorganize(self, df):
        """
        Post processing for the data fetching result
        include:
               - reorganizing on columns according to its original req sequence
                * cwp field will follow closely with its host field
               - removing hidden columns
                * calculated field will need some hidden fields sending to
                  data-source to help computing
               - resort on rows
                * the original sorting field is not data-source native field
                  need sorting the data rows here
        """

        def _sort_func(col, cols):
            """
            Args:
                col(string): sorting item
                cols(list): the sorting sequence list
            Returns(int or float): sorting order
            """
            if col in cols:
                return cols.index(col)
            elif col.endswith(':cwp'):
                # cwp field need follow closely with its host,
                # so its order will be a bit bigger than its host
                return cols.index(col[:-4]) + .1
            return float('inf')

        columns = list(df)
        columns_reorganized = sorted(columns, key=lambda _: _sort_func(_, self.params.seq))
        to_remove = [col for col in columns_reorganized if col.startswith('hidden_field')]
        # reorganize column sequence & remove hidden columns
        df = df.reindex(columns=columns_reorganized).drop(to_remove, axis=1, inplace=False)

        if self.resort:
            sort_by = self.params.sort['field']['uuid']
            ascending = not self.params.sort['order'] == 'desc'
            if self.include_summary:
                summary_df = df.tail(1)
                data_df = df.head(len(df) - 1)
                data_df.sort_values(by=sort_by, ascending=ascending, inplace=True)
                df = data_df.append(summary_df)
            else:
                df.sort_values(by=sort_by, ascending=ascending, inplace=True)

        # analyze function on fields
        result_df = self.do_analyze(df)
        return result_df

    def post_header_fill(self):
        """headers return back with data"""

        def _sort_func(field, cols):
            if field['uuid'] in cols:
                return cols.index(field['uuid'])
            elif field['uuid'].endswith(':cwp'):
                # cwp field need follow closely with its host,
                # so its order will be a bit bigger than its host
                return cols.index(field['uuid'][:-4]) + .1
            return float('inf')

        fields = self.params.fields or []
        cwp_fields = self.params.compareWithPrevious.get('fields', [])
        for cwp_f in cwp_fields:
            cwp_f['uuid'] += ":cwp"
        cal_fields = self.params.calculatedFields or []
        all_fields = fields + cwp_fields + cal_fields
        return sorted(
            all_fields,
            key=lambda _: _sort_func(_, self.params.seq)
        )

    def get_result(self):
        """ helper method to trigger FetchingDataHandler, and decorate the result"""
        df = self.post_reorganize(self.execute())

        # change np.nan back to None
        all_data = df.where(df.notnull(), None).values.tolist()

        # split the data rows: the last row in the 2-dimension-lists is the summary value
        if self.include_summary:
            data_rows = all_data[:-1]
            summary_row = all_data[-1]
        else:
            data_rows = all_data
            summary_row = [None for _ in range(len(data_rows[0]))] if data_rows else []

        extra_info = {}
        if self.cwp_date_range:
            extra_info['cwp_date_range'] = self.cwp_date_range

        result = {
            'header': self.post_header_fill(),
            'data': data_rows,
            'summaryValues': summary_row,
        }

        if extra_info:
            result['extra_info'] = extra_info
        return result
