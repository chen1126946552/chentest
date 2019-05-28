"""All classes/methods/tools to help to adapt to v2 on `calculated fields`"""
from uuid import uuid1
from copy import deepcopy
from .constant import Fields

DATA_TYPE_MAP = {
    # vx-field: v2-field
    "number": "INTEGER",
    "string": "STRING",
    "date": "DATETIME",
    "percentage": "PERCENT",
    "durationInSeconds": "DURATION",
    "currency": "CURRENCY"
}


DATA_TYPE_MAP_REVERSE = {
    # v2-field: vx-field
    "INTEGER": "number",
    "STRING": "string",
    "DATETIME": "date",
    "PERCENT": "percentage",
    "DURATION": "durationInSeconds",
    "CURRENCY": "currency"
}


def calculated_field_data_adapt(cal_fields):
    """adapt vx calculated fields to v2, in showing list records"""

    def data_format(candidates):
        # vx's data-format is to v2's data-type
        data_formats = [c.get('displayFormat') for c in candidates]
        # assert len(data_formats) == 1
        if "durationInSeconds" in data_formats:
            # only if all candidates are all duration formats, the cal field is a 'duration' field
            # otherwise, it is a number field
            if len(set(data_formats)) == 1:
                return "durationInSeconds"
        return "number"

    def _parse_cal_field(calf):
        candidates = calf['fields']
        dfmt = data_format(candidates)
        dtype_for_v2 = DATA_TYPE_MAP.get(dfmt)
        return {
            "id": calf['id'],
            "uuid": None,
            "fieldId": calf['id'],
            "name": calf['name'],
            # Vnext's dataFormat is response to to v2's dataType
            "dataType": dtype_for_v2,
            "calculateType": None,
            "dataFormat": dfmt,
            "validateStatus": "1",
            "extra": {
                "allowFilter": 0 if not calf['allow_filter'] else 1,
                "containGroupFunction": calf['group_function_contain'],
                "code": calf['id'],
                "type": "compoundMetrics",
                "allowGroup": False
            },
            "columnType": None,
            "alias": None,
            "granularity": None,
            "type": None,
            "labelName": None,
            "analysisFunctionType": None,
            "dataScope": None,
            "containFunction": calf['function_contain'],
            "showName": calf['display']
        }

    return {
        "success": True,
        "data": [
            _parse_cal_field(calf) for calf in cal_fields
        ]
    } if isinstance(cal_fields, list) else {
        "success": True,
        "data": _parse_cal_field(cal_fields)
    }


def calculated_field_editor_data_adapt(calf):
    """adapt vx calculated fields to v2, in editing/saving single record

    According to observation, `formula`, original_aggregator
    are always the same in v2 database.  They are formatted expression
    that field ids replaced with a new-created uuids. But in vnext,
    we might not need to do that any longer... so, just expression is enough

    `aggregator` is the actual expression that display in the input box
    """

    fields = calf['fields']
    for field in calf['fields']:
        field['formulaId'] = str(uuid1())
        field['fieldId'] = field['id']

    expression = calf['expression']

    key_name_map = {"$id_" + f['id']: f['name'] for f in fields}

    key_formula_map = {"$id_" + f['id']: f['formulaId'] for f in fields}

    aggregator = formula = expression

    for k, v in key_name_map.items():
        aggregator = aggregator.replace(k, f'`{v}`')

    for k, v in key_formula_map.items():
        formula = formula.replace(k, f'`{v}`')

    original_aggregator = formula

    result = {
        "id": calf['id'],
        "name": calf['name'],
        "code": calf['id'],
        "formula": formula,
        "aggregator": aggregator,
        "originalAggregator": original_aggregator,
        "description": "",
        "spaceId": None,
        "dsConnectionId": None,
        "items": fields,
        "uid": None,
        "userEmail": None,
        "dataType": DATA_TYPE_MAP.get(calf['type'], calf['type']),
        "dataFormat": None,
        "unit": None,
        "dsId": None,
        "dsCode": None,
        "connectionId": calf['connection'],
        "tableId": None
    }

    return {
        "data": result,
        "success": True
    }


def calculated_field_params_parse(params):
    """parse v2 calculated fields to vx"""
    expression = params['originalAggregator']
    keys_map = {}
    fields = {}
    for item in params['items']:
        keys_map[item['formulaId']] = item['id']
        vx_field = _field_parse(item)
        fields[vx_field['id']] = vx_field

    for k, v in keys_map.items():
        expression = expression.replace(f"`{k}`", f"$id_{v}")

    return {
        'expression': expression,
        'candidates': list(fields.values()),
        'name': params['name']
    }


def calculated_field_candidates_filter(fields):
    """filter the calculate candidates, only metrics(number field) could be selected"""
    def parse(f):
        if 'children' not in f:
            return deepcopy(f) if f.get('type') == 'number' else None
        new_f = deepcopy(f)
        children = [_ for _ in [parse(child) for child in new_f['children']] if _]
        new_f.update({'children': children})
        return new_f if children else None
    return [_ for _ in [parse(field) for field in fields] if _]


def _field_parse(v2_field):
    """helper method, parse single calculated field v2 to vx"""
    vx_field = dict()
    vx_field['id'] = v2_field['id']
    vx_field['name'] = v2_field['name']
    vx_field['type'] = Fields.NameMapping.type_map.get(v2_field['dataType'])
    vx_field['displayFormat'] = DATA_TYPE_MAP_REVERSE.get(v2_field.get('dataType', ''), None)
    vx_field['allowFilter'] = v2_field.get('allFilter') == 1
    vx_field['allowGroupby'] = v2_field.get('allowGroup', False)
    vx_field['allowSegment'] = v2_field.get('allowSegment') == 1
    return vx_field
