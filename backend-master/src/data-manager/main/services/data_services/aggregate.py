"""Aggregate handler"""

import pandas as pd

AGG_MAP = {
    'sum': 'sum',
    'average': 'mean',
    'min': 'min',
    'max': 'max',
    'stdev': 'std',
    'var': 'var',
    'counta': 'count',
    'dcount': 'nunique'
}


class AggregateHandler:
    """Group and aggregation calculations handler """

    def __init__(self, data_frame, req_body):
        self.data_frame = data_frame
        self.fields = req_body.fields
        self.sort = req_body.sort

    def get_date_fields(self):
        """Gets date type filed"""
        return [field['uuid'] for field in self.fields if field.get('groupBy')
                and field.get('type') == 'date']

    def get_dimension_fields(self):
        """Gets dimension fields"""
        return [field['uuid'] for field in self.fields if field.get('groupBy')]

    def get_metric_fields(self):
        """Gets metric fields"""
        return [field['uuid'] for field in self.fields if not field.get('groupBy')]

    def get_agg_field_map(self):
        """Gets field function map"""
        result = {}
        for field in self.fields:
            if field.get('groupBy') is None and field.get('agg'):
                result[field['uuid']] = AGG_MAP[field['agg']]
        return result

    def _do_sort(self, data_obj):
        """
        Result data sort
        Args:
            data_obj: Pandas's Series or DataFrame
        """
        if self.sort:
            order_asc = bool(self.sort.get('order', 'asc') == 'asc')
            order_field = self.sort['field']['uuid']
            if isinstance(data_obj, pd.DataFrame):
                data_obj.sort_values(by=order_field, ascending=order_asc, inplace=True)
            elif isinstance(data_obj, pd.Series):
                data_obj.sort_values(ascending=order_asc, inplace=True)

    def execute(self):
        """grouping and aggregation calculations"""

        group_ids = self.get_dimension_fields()
        metric_ids = self.get_metric_fields()
        summary_values = self.get_summary_values()
        pandas_obj = self.data_frame
        if not metric_ids:
            self.data_frame.drop_duplicates(inplace=True)
        elif not group_ids:
            pandas_obj = self.data_frame.agg(self.get_agg_field_map())
        else:
            pandas_obj = self.data_frame.groupby(group_ids)\
                .agg(self.get_agg_field_map()).reset_index()

        self._do_sort(pandas_obj)
        data_list = []
        if isinstance(pandas_obj, pd.Series):
            data_list.append(pandas_obj.values.tolist())
        else:
            data_list.extend(pandas_obj.values.tolist())
        return {
            'data': data_list,
            'summaryValues': summary_values
        }

    def get_summary_values(self):
        """Gets summary values"""
        metric_fields = self.get_metric_fields()
        values = []
        if metric_fields:
            result_df = self.data_frame.agg(self.get_agg_field_map())
            for data in result_df.values.tolist():
                values.append(round(float(data), 2))
        return values

    def _convert_date_by_granularity(self):
        pass
