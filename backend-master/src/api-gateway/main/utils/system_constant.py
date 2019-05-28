"""
System constant definition
"""
from services.downstream import get_datasources

# TODO: give cache an expiration period

# VNext ds code list
_VNEXT_DS_CODE_LIST = []
# VNext ds_code => ds_id map
_VNEXT_DS_CODE_ID_MAP = {}
# VNext ds_id =>ds_code  map
_VNEXT_DS_ID_CODE_MAP = {}
# key: ds_id|ds_code, value: ds_info_dict
_VNEXT_DS_INFO_MAP = {}


TYPE_METRICS = "metrics"
TYPE_COMPOUND_METRICS = "compoundMetrics"
TYPE_DIMENSION = "dimension"
TYPE_COMPOUND_DIMENSION = "compoundDimension"


def get_ds_info_by_ds_id(ds_id):
    """
    Cache ds info map
    Args:
        ds_id (int): ds_id
    Returns: (dict) ds info

    """
    if isinstance(ds_id, str) and ds_id.isnumeric():
        ds_id = int(ds_id)
    if not _VNEXT_DS_INFO_MAP:
        load_ds_config()
    return _VNEXT_DS_INFO_MAP.get(ds_id)


def get_ds_info_by_ds_code(ds_code):
    """
    Gets datasource info by its code

    Args:
        ds_code (str): datasource code

    Returns: (dict) ds info
    """
    ds_id = get_ds_id_by_code(ds_code)
    return get_ds_info_by_ds_id(ds_id)


def get_ds_code_list():
    """
    Cache vn dataSource ds code list
    Returns:
        ds code list
    """
    if not _VNEXT_DS_CODE_LIST:
        load_ds_config()
    return _VNEXT_DS_CODE_LIST


def get_ds_code_by_id(ds_id):
    """
    Get the dsCode by dsId
    Args:
        ds_id: ds id
    Returns:
        ds code
    """
    if not _VNEXT_DS_ID_CODE_MAP:
        load_ds_config()
    return _VNEXT_DS_ID_CODE_MAP.get(ds_id)


def get_ds_id_by_code(ds_code):
    """
    Get the dsId by dsCode
    Args:
        ds_code: ds code
    Returns:
        ds id
    """
    if not _VNEXT_DS_CODE_ID_MAP:
        load_ds_config()
    return _VNEXT_DS_CODE_ID_MAP.get(ds_code)


def load_ds_config():
    """Load ds config by data-manage service"""
    clear_all_cache()
    ds_config_list = get_datasources()
    if ds_config_list:
        for ds_config in ds_config_list:
            ds_code = ds_config["code"]
            ds_id = ds_config["ds_id"]
            _VNEXT_DS_CODE_LIST.append(ds_code)
            _VNEXT_DS_CODE_ID_MAP[ds_code] = ds_id
            _VNEXT_DS_ID_CODE_MAP[ds_id] = ds_code
            _VNEXT_DS_INFO_MAP[ds_id] = ds_config
            _VNEXT_DS_INFO_MAP[ds_code] = ds_config


def clear_all_cache():
    """
    Clear all data
    """
    _VNEXT_DS_CODE_LIST[:] = []
    _VNEXT_DS_CODE_ID_MAP.clear()
    _VNEXT_DS_ID_CODE_MAP.clear()
    _VNEXT_DS_INFO_MAP.clear()


class DataFormat:
    """Data format definition"""
    PERCENTAGE = "percentage"
    DURATION_IN_SECONDS = "durationInSeconds"


class DataType:
    """Data type constant"""
    NUMBER = "NUMBER"
    DOUBLE = "DOUBLE"
    TEXT = "TEXT"
    DATE = "DATE"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    TIME = "TIME"
    PERCENT = "PERCENT"


class DatePeriod:
    """Date type period"""
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"
    SECONDS = "seconds"
    QUARTER = "quarter"
    WEEK = "week"

    PERIOD_FORMAT_DICT = {
        YEAR: "yyyy",
        MONTH: "yyyy-MM",
        DAY: "yyyy-MM-dd",
        HOUR: "yyyy-MM-dd HH",
        MINUTE: "yyyy-MM-dd HH:mm",
        SECONDS: "yyyy-MM-dd HH:mm:ss",
    }

    @classmethod
    def get_format_by_period(cls, date_period):
        """Gets format expression by period"""
        if date_period:
            date_period_lower = date_period.lower()
            return cls.PERIOD_FORMAT_DICT.get(date_period_lower)
        return None


class Func:
    """Aggregate function constant"""
    FUNC_SUM = "SUM"
    FUNC_MAX = "MAX"
    FUNC_MIN = "MIN"
    FUNC_AVERAGE = "AVERAGE"
    FUNC_AVG = "AVG"
    FUNC_COUNTA = "COUNTA"
    FUNC_COUNTUNIQUE = "COUNTUNIQUE"
    FUNC_D_COUNT = "D_COUNT"
    FUNC_STDEV = "STDEV"
    FUNC_VARIANCE = "VAR"
