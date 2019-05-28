"""Data field analyze function"""
from functools import reduce
from services.exceptions import ServiceError
from services.common import Constant

# pylint: disable=invalid-name


class AnalyzeDataHandler:
    """Analyzing feature handler"""

    def __init__(self, data_frame, cols_operation_map, group_by_columns):
        """
        Args:
            data_frame(pd.DataFrame):
                the data rows containing the summary row which located at the last row
            cols_operation_map(dict):
                column: operation code e.g {'column1': 'proportion'}
            dm_cnt:
        """
        self.data_frame = data_frame
        self.operation_map = cols_operation_map
        self.group_by_columns = group_by_columns

    def execute(self, inplace=True):
        """Handler trigger"""
        df = self.data_frame.copy(deep=not inplace)
        if df.empty:
            return df
        for col, operation in self.operation_map.items():
            if not hasattr(self.__class__, operation):
                raise ServiceError('Unsupported analyze code: %s' % operation)
            # a temp data frame containing all dimension columns and the target metric column
            temp_df = df.loc[:, self.group_by_columns + [col]]
            new_col_values = getattr(self.__class__, operation)(temp_df)
            df[col] = new_col_values
        return df

    @classmethod
    def cumulate(cls, partial_df):
        """the cumulate value for each number in the whole column
        the logic here is that with different first dimension
        but the same other dimensions, computing the sum of all
        the previous values.
        """
        last_column_values = partial_df.iloc[:, -1]

        def _compute(i, j):
            try:
                return i + j
            except Exception:  # pylint: disable=broad-except
                return None

        def _reduce(rows):
            if not rows:
                return None
            return reduce(lambda i, j: _compute(i, j), rows)  # pylint: disable=unnecessary-lambda

        def match(s1, s2):
            """compare two series, ignore the first dimension and last target metric"""
            return s1[1:-1].equals(s2[1:-1])

        def _find_rows(idx):
            row = partial_df.iloc[idx]
            row_pools = partial_df.iloc[range(idx + 1)]
            # find all the matched previous numbers
            return [v[-1] for k, v in row_pools.iterrows() if match(v, row)]

        result = [_reduce(_find_rows(idx)) for idx in range(len(last_column_values))]
        result[-1] = None
        # the summary value is None(N/A)
        return result

    @classmethod
    def proportion(cls, partial_df):
        """compute proportion of each number in the whole column"""
        last_column_values = partial_df.iloc[:, -1]
        total = sum([i for i in last_column_values[:-1] if isinstance(i, (float, int))])

        def _compute(cur):
            try:
                return round(float(cur) / total, Constant.Data.COMPUTING_PRECISION)
            except Exception:  # pylint: disable=broad-except
                return None
        result = [_compute(me) for me in last_column_values]
        # the summary value is None(N/A)
        result[-1] = None
        return result

    @classmethod
    def growth_rate(cls, partial_df):
        """compute growth rate of each number in the whole column
        the logic here is that with different first dimension but
        the same other dimensions, the metric growth rate comparing
        to its previous value
        """
        last_column_values = partial_df.iloc[:, -1]

        def _compute(cur, pre):
            try:
                return round(float(cur - pre) / pre, Constant.Data.COMPUTING_PRECISION)
            except Exception:  # pylint: disable=broad-except
                return None

        def match(s1, s2):
            """compare two series, ignore the first dimension and last target metric"""
            return s1[1: -1].equals(s2[1: -1])

        def _find_value_in_target_row(idx):
            row = partial_df.iloc[idx]
            row_pools = partial_df.iloc[range(idx)]
            row_pools.reindex(index=row_pools.index[::-1])
            try:
                # find the first match previous number
                return next(v[-1] for k, v in row_pools.iterrows() if match(v, row))
            except StopIteration:
                return None

        result = [_compute(last_column_values[idx], _find_value_in_target_row(idx)) for idx in
                  range(len(last_column_values))]
        # the summary value is None(N/A)
        result[-1] = None
        return result
