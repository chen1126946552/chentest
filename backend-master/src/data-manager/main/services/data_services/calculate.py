"""calculated field handle for secondary calculation"""
import string
import random
import logging
import traceback
import ast
import importlib
import inspect
from copy import deepcopy
from functools import reduce
from collections import namedtuple
import pandas as pd
import numpy as np
from ._basic_calculating_ns import GLOBAL_NAME_SPACE

# pylint: disable=invalid-name,missing-docstring

logger = logging.getLogger(__name__)
BASE_CALLABLE_SUPPORTED = {}
GROUP_FUNCTION_IDENTIFIERS = ['Sum', 'Avg', 'Max', 'Min', 'Count', 'Distinct_count']
IDENTIFIER = 'function_identifier_produced_by_exprParser'
COLUMN_PREFIX = 'new_column_prefix_produced_by_Pandas'
VAR_NAME_LENGTH = 5

# function container
Function = namedtuple(
    'Function',
    ('identifier', 'args')
)


def _get_py_variable_names(n):
    """make n random legal name for python"""
    make_py_variable_name = lambda: "".join(
        random.sample(string.ascii_lowercase, VAR_NAME_LENGTH))
    names, cnt = [], 0
    while cnt < n:
        name = make_py_variable_name()
        if name not in names:
            names.append(name)
            cnt += 1
    return names


class CalculatedDataHandler:
    """calculated field function handler"""

    def __init__(self, data_frame, fields, cal_fields):
        """
        Args:
            data_frame (pd.DataFrame): data frame with columns are fields' uuids
            fields (list): fields for data frame columns
            cal_fields (list[dict]): calculated fields containing expression
            and candidates fields information
        """
        self.data_frame = data_frame
        self.fields = fields
        self.cal_fields = cal_fields

    @classmethod
    def get_function(cls, expr, keys_mapping):
        """
        Get the constructed function for expression in datafram
        Args:
            expr(string): expression string e.g. $id_field1 + ceil($id_field2 * 2)
            keys_mapping (dict): a map that mapping field in expr to py legal variable names
        Returns (namedtuple): function container

        """
        parser = ExpressionParser(expr, keys_mapping)
        identifier = parser.function
        args = parser.args
        return Function(identifier=identifier, args=args)

    # pylint: disable= too-many-locals
    def execute(self, inplace=True):
        # computing expression, add new computed columns into dataframe

        cal_cols = [calf['uuid'] for calf in self.cal_fields]

        if self.data_frame.empty:
            df = self.data_frame.copy(deep=not inplace)
            for c_col in cal_cols:
                df[c_col] = None
            return df

        expressions = [calf['expression'] for calf in self.cal_fields]
        cal_keys = reduce(lambda i, j: list(i) + list(j),
                          [calf['keys'] for calf in self.cal_fields])

        columns_back_up = list(self.data_frame)
        rename_columns = [f['id'] for f in self.fields]
        assert len(columns_back_up) == len(rename_columns)
        self.data_frame.columns = rename_columns
        assert all(key in self.data_frame for key in cal_keys)

        cols = list(self.data_frame)
        keys_mapping = dict(
            zip(['$id_' + key for key in cal_keys], _get_py_variable_names(len(cal_keys))))
        rename_columns = [keys_mapping.get("$id_" + k, k) for k in self.data_frame]

        assert len(rename_columns) == len(cols)
        self.data_frame.columns = rename_columns
        temp_df = self.data_frame.loc[:, ~self.data_frame.columns.duplicated()]

        funcs = [self.get_function(expr, keys_mapping) for expr in expressions]

        df = self.data_frame.copy(deep=not inplace)
        # pylint: disable=cell-var-from-loop
        for idx, func in enumerate(funcs):
            df[cal_cols[idx]] = \
                temp_df.apply(lambda row: func.identifier(*tuple(row[arg] for arg in func.args)),
                              axis=1)
        df.columns = columns_back_up + cal_cols
        return df

    @classmethod
    def check_calf_expression(cls, expr, keys):
        """
        check if an expression is ok
        Args:
            expr(string): $id_field1 + ceil($id_field2) / $id_field3
            keys(list): [field1, field2, field3]
        Returns:
            if ok, return analytics of the expression, else, return None
        """

        def make_test_field(fid):
            """fabricate a field for expression invalidating"""
            return {
                'id': fid,
                'uuid': fid,
                'type': 'number'
            }

        def make_test_cal_field(fid, _keys, _expr):
            """fabricate a calculated field for expression invalidating"""
            base_field = make_test_field(fid)
            base_field.update({
                'keys': _keys,
                'expression': _expr
            })
            return base_field

        try:
            # prepare testing data
            test_data = np.random.rand(10, len(keys)).tolist()
            keys_mapping = dict(
                zip(['$id_' + key for key in keys], _get_py_variable_names(len(keys))))
            df = pd.DataFrame(data=test_data, columns=keys)

            # prepare testing fields/cal-fields
            test_fields = [
                make_test_field(key) for key in keys
            ]
            test_cal_fields = [make_test_cal_field('what_ever', keys, expr)]

            # executing validating, no exception indicates passing the validating
            _ = CalculatedDataHandler(
                data_frame=df, fields=test_fields, cal_fields=test_cal_fields
            ).execute(inplace=True)

            info = ExpressionParser(expr, keys_mapping).expression_analysis()
            return info
        except Exception:  # pylint: disable=broad-except
            logger.error("Calculated field expression check failed, %s %s %s", expr, keys,
                         traceback.format_exc())
            return None


class ExpressionTransformer(ast.NodeTransformer):
    """py ast node transformer"""

    def __init__(self, calls_supported_map):
        self.calls_supported_map = calls_supported_map
        super(ExpressionTransformer, self).__init__()

    def visit_Call(self, node):
        """replace the callable's name with supported standard name"""
        if node.func.id not in self.calls_supported_map:
            raise ValueError('Unsupported function: %s' % node.func.id)
        node.func.id = self.calls_supported_map[node.func.id]
        return node


class ExpressionVisitor(ast.NodeVisitor):
    """py ast node visitor to collecting node information when traversing the tree"""

    def __init__(self, *args, **kwargs):
        super(ExpressionVisitor, self).__init__(*args, **kwargs)
        self._names = []
        self._func_identifiers = []

    @property
    def names(self):
        """property helper method"""
        return self._names

    @property
    def func_identifiers(self):
        """property helper method"""
        return self._func_identifiers

    def visit_Name(self, node):
        """collecting variable names"""
        self.names.append(node.id)

    def visit_Call(self, node):
        """collecting function identifiers"""
        self.func_identifiers.append(node.func.id)


class ExpressionParser:
    """expression parser, used to parse/analyze expression,
    and construct a function with input expression. e.g for expression a + b * b + 5
    we need construct a method with global variable `IDENTIFIER` to
    ```
        def foo(a, b):
            return a + b * b + 5
    ```
    """

    def __init__(self, expr, keys_mapping, modules_supported="math,"):
        """
        Args:
            expr(string): input expression `$id_field1 + ceil($id_field2)`
            keys_mapping(dict): because the expression may have names that can not passed by py ast
                    so must offer an keys map to replace the illegal name with a legal one
                    e.g. $id_field1 is not ok with python as a variable name/argument
                    so an keys map like {'$id_field1': 'foo', '$id_field2': 'bar'} need offered
            modules_supported(str):
                    functions may contained in expression

        """
        self.expr = expr
        self.key_map = keys_mapping
        self.modules = modules_supported
        self._process()

    def _process(self):
        """a helper method to initialize expression parser"""
        # exec_namespace is dict as a namespace where the constructed function would run in
        self.exec_namespace = deepcopy(GLOBAL_NAME_SPACE)
        self.key_map_reversed = self._make_key_map_reversed()
        self.body = self._make_func_body()
        self._reload_namespace()
        try:
            # parsing expression, change the unstandard function names
            _root = ast.parse(self.body)
            self.root = ExpressionTransformer(calls_supported_map=self.exec_namespace).visit(_root)
            logger.debug('Tampering the calculated expression ast: %s', ast.dump(self.root))
        except Exception:  # pylint: disable=invalid-name,broad-except
            logger.error("Parse expression failed: %s", self.body)
            raise

    def _reload_namespace(self):
        """update the exec_namespace where the constructed function would run"""
        mod_names = [_.strip() for _ in self.modules.split(',') if _]
        mods = [importlib.import_module(mod_name) for mod_name in mod_names]
        callables = reduce(lambda i, j: i + j,
                           [[member[1] for member in inspect.getmembers(mod) if callable(member[1])]
                            for mod in mods])
        self.exec_namespace.update({c.__name__: c for c in callables})

    def _make_func_body(self):
        """replace the illegal names in expression with normal py names"""
        source = self.expr
        for k, v in self.key_map.items():
            source = source.replace(k, v)
        return source

    def _make_key_map_reversed(self):
        """helper method to reserve the keys map"""
        return {v: k for k, v in self.key_map.items()}

    def _make_args(self):
        """get the constructed function's arguments set"""
        cv = ExpressionVisitor()
        cv.visit(self.root)
        args = cv.names
        return sorted({arg for arg in args if arg in self.key_map_reversed}, key=args.index)

    def _make_func(self):
        """get the constructed function's executable object"""
        # todo need time to investigate how to insert a new ast root
        # todo instead of parse a string
        args_str = ",".join(self._make_args())
        func_expression = f"""
def {IDENTIFIER}({args_str}):
    try:
        return {self.body}
    except ZeroDivisionError:
        return 0
    except Exception:
        return None"""
        root = ast.parse(func_expression, mode='exec')
        code = compile(root, filename='<string>', mode='exec')
        try:
            # pylint: disable=exec-used
            exec(code, self.exec_namespace)
        except Exception:  # pylint: disable=invalid-name,broad-except
            logger.error("Generate Function failed: %s", func_expression)
            raise

    @property
    def function(self):
        """property helper method"""
        if IDENTIFIER not in self.exec_namespace:
            self._make_func()
        return self.exec_namespace[IDENTIFIER]

    @property
    def args(self):
        """property helper method"""
        return self._make_args()

    def expression_analysis(self):
        """expression analysis, checking function/agg function containing"""
        cv = ExpressionVisitor()
        cv.visit(self.root)
        funcs = [f.lower() for f in set(cv.func_identifiers)]
        return {
            'function_contain': bool(funcs),
            'group_function_contain': any(g_func in funcs for g_func in GROUP_FUNCTION_IDENTIFIERS)
        }
