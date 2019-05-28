"""Data manager data service metadata"""
from dataclasses import dataclass, field

# pylint: disable=invalid-name


@dataclass  # pylint: disable=too-many-instance-attributes
class ParsedParams:
    """
    Class for data req params from upstream(Business layer)
    """

    token: dict = None
    path: list = None
    locale: str = None
    timezone: str = None
    weekStartOn: str = None
    paging: list = field(default_factory=list)
    filters: list = field(default_factory=list)
    dateRange: dict = field(default_factory=dict)
    sort: dict = field(default_factory=dict)
    segment: dict = field(default_factory=dict)
    fields: list = field(default_factory=list)
    calculatedFields: list = field(default_factory=list)
    seq: list = field(default_factory=list)
    compareWithPrevious: dict = field(default_factory=dict)
    graphType: dict = None
    map: dict = None
    noCache: bool = False
    dsInfo: dict = field(default_factory=dict)


@dataclass  # pylint: disable=too-many-instance-attributes
class ParsedReqBody:
    """
    Class for data req body to downstream(Data-Source layer)
    """
    token: dict = None
    path: list = None
    locale: str = None
    timezoneOffset: int = 0
    paging: list = None
    filters: list = None
    dateRange: dict = None
    sort: dict = None
    segment: dict = None
    fields: list = None
    calculatedFields: list = None
