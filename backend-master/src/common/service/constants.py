"""
Constants shared by multiple services in the stack.
"""
from enum import Enum

class DatasourceTypes:
    """
    Datasource types.
    """

    API = 'api'
    DB = 'db'
    FILE = 'file'



class GraphType(Enum):
    """
    Widget Graph Type

    """

    LINE = 'line'
    AREA = 'area'
    STACKCOLUMN = 'stackColumn'
    STACKBAR = 'stackBar'
    DOUBLEAXIS = 'doubleAxis'
    AREASPLINE = 'areaspline'
    COLUMN = 'column'
    BAR = 'bar'
    PIE = 'pie'
    NUMBER = 'number'
    PROGRESSBAR = 'progressbar'
    TABLE = 'table'
    MAP = 'map'
    FUNNELBYCATEGORY = 'funnelByCategory'
    FUNNELBYMETRICS = 'funnelByMetrics'
    BUBBLE = 'bubble'
    SCATTERPLOT = 'scatterPlot'

    def is_highchart(self):
        return self in [
            GraphType.LINE,
            GraphType.AREA,
            GraphType.STACKCOLUMN,
            GraphType.STACKBAR,
            GraphType.AREASPLINE,
            GraphType.DOUBLEAXIS,
            GraphType.COLUMN,
            GraphType.BAR,
            GraphType.PIE,
            GraphType.MAP,
            GraphType.FUNNELBYCATEGORY,
            GraphType.FUNNELBYMETRICS,
            GraphType.BUBBLE,
            GraphType.SCATTERPLOT]

    def is_map(self):
        return GraphType.MAP == self


class CommonHeaders:
    """
    Standard HTTP headers used across services.
    """
    LOCALE = 'Accept-Language'
    TIMEZONE = 'Timezone'
