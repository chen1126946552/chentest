"""All classes/methods/tools to help to adapt to v2 `segments`"""

TYPE_KEY = 'type'
IS_CUSTOM_KEY = 'is_custom'


def segments_result_data_adapt(segments, ds_code):
    """
    adapt vx fields to v2 fields
    Args:
        segments(list): vx segments
        ds_code(string): ds code
    Returns(list): v2 segments
    """
    v2_segments = [seg for seg in segments]
    for v2_seg in v2_segments:
        if v2_seg.get(IS_CUSTOM_KEY):
            v2_seg[TYPE_KEY] = None
        else:
            v2_seg[TYPE_KEY] = ds_code
    return v2_segments


def get_segments_id_name_map(segments):
    """
    recursive get fields id:name map
    Args:
        fields(list): VNEXT field property
    Returns(dict): id:name map

    """
    result_map = {}
    for seg in segments:
        result_map[seg['id']] = seg['name']
    return result_map
