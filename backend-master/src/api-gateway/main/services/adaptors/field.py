"""All classes/methods/tools to help to adapt to v2 `FIELDS`"""

import copy


def fields_result_data_adapt(fields):
    """
    adapt vx fields to v2 fields
    Args:
        fields: [list] v2 fields
    Returns: [list] vx fields
    """
    data_type_map = {
        # vx-field to v2-field
        "number": "INTEGER",
        "string": "STRING",
        "date": "DATETIME",
        "percentage": "PERCENT",
        "durationInSeconds": "DURATION",
        "currency": "CURRENCY"
    }

    # pylint: disable=invalid-name
    def parse(vx):
        v2 = {
            'id': vx.get('id'), # group node may not have 'id' field
            'name': vx['name']
        }
        if vx.get('children') is None:
            # field
            v2['dataType'] = data_type_map.get(vx['type'], vx['type'])
            if 'displayFormat' in vx:
                display_format = vx['displayFormat']
                if 'numberFormat' in display_format:
                    v2['dataFormat'] = display_format['numberFormat']
                    v2['dataType'] = data_type_map.get(display_format['numberFormat'])
                elif 'granularity' in display_format:
                    v2['dataFormat'] = display_format['granularity']

            # TODO v2 field's 'granularity' is a selected front-end controls, not supported for GA
            # it has nothing to do with vnext's granularity which is a native attribute of one field
            v2['granularity'] = None
            v2['code'] = vx['id']
            v2['allowFilter'] = 1 if vx.get('allowFilter') else 0
            v2['allowGroup'] = vx.get('allowGroupby', False)
            v2['allowScope'] = None
            v2['allowSegment'] = 1 if vx.get('allowSegment') else 0
            v2['containGroupFunction'] = False
            v2['defaultScope'] = None
            v2['skipExistCheck'] = None
            v2['fieldId'] = vx['id']
            v2['uuid'] = None
            v2['validateStatus'] = "1"
            v2['extra'] = {
                "allowFilter": 1 if vx.get('allowFilter') else 0,
                "allowGroup": vx.get('allowGroupby', False),
                # TODO: for now allow aggregation considers both flags; moving forward
                # it should solely respect 'allowAggregation' field from datasource
                "allowAggregation": vx.get('allowAggregation', False) or \
                    not vx.get('allowGroupby', False),
                "allowScope": None,
                "allowSegment": 1 if vx.get('allowSegment') else 0,
                "code": vx['id'],
                "containGroupFunction": False,
                "defaultScope": None,
                "skipExistCheck": None,
                "type": 'dimension' if vx.get('allowGroupby') else 'metrics'
            }
        else:
            # folder
            v2['code'] = ''
            v2['extra'] = None
            if vx.get('children') is not None:
                v2['child'] = [parse(vx_child) for vx_child in vx['children']]
            if not v2['child']:
                # skip empty folder
                return None
        return v2

    return {
        "id": -1,
        "name": None,
        "code": None,
        "extra": None,
        "child": list(filter(None, (parse(item) for item in fields)))
    }


def filter_fields_result_data_adapt(fields):
    """adapt filter fields to v2"""
    return fields_result_data_adapt(_filter_allowed_fields_filtering(fields))


def _filter_allowed_fields_filtering(fields):
    """recursively filtered the filter-none-allowed fields"""
    filter_allowed_fields = []
    for field in fields:
        if not field.get('allowFilter'):
            continue
        new_field = copy.deepcopy(field)
        if 'children' in field:
            new_field['children'] = _filter_allowed_fields_filtering(new_field['children'])
        filter_allowed_fields.append(new_field)
    return filter_allowed_fields


def get_fields_id_name_map(fields):
    """
    recursive get fields id:name map
    Args:
        fields(list): VNEXT field property
    Returns(dict): id:name map

    """
    result_map = {}
    for field in fields:
        if 'children' in field:
            result_map.update(get_fields_id_name_map(field['children']))
        else:
            result_map[field['id']] = field['name']
    return result_map
