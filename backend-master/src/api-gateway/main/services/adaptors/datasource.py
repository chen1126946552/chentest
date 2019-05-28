"""All classes/methods/tools to help to adapt to v2 on `datasource`"""

import logging

from common.http.utils import ApiError
from services.downstream import get_datasource_config
from utils.system_constant import get_ds_id_by_code

logger = logging.getLogger(__name__)


def dslist_result_data_adapt(items):
    """
    adapt v2 ds list
    Args:
        items: [list] vx datasources
    Returns: [list] datasources adapt to v2
    """
    ds_list_after_mixin = []
    for item in items:
        data = ds_single_data_adapt(item)
        if data:
            ds_list_after_mixin.append(data)
    return ds_list_after_mixin


def ds_single_data_adapt(data_source):
    """
    Adapt v2 single ds object
    Args:
        datasource: VNext ds

    Returns: datasource
    """
    data = {}

    ds_code = data_source['code']

    try:
        # v2 `oauth` auth-type is supposed to be 'saas'
        auth_type = get_datasource_config(ds_code).get('auth', {}).get('type', None) or 'saas'
    except ApiError:
        logger.error('Unable to get config for datasource %s', ds_code)
        return None

    data['authType'] = auth_type if auth_type != 'oauth' else 'saas'
    # category, same with authType, not handle yet
    if auth_type == 'form':
        data['category'] = 'rdatabase'
        data['dataSourceType'] = 'db'
        config = {}
        config['canCreateDatasetByConnection'] = 1
        config['canEditConnection'] = 1
        config['canEditSchema'] = 1
        config['canUpdateSchema'] = 1
        config['isTreeMenu'] = 1
        data['config'] = config
    else:
        data['category'] = data['authType']
        data['dataSourceType'] = 'saas'
    # v2 dsId is fixed to represent what datasource it is
    data['dsId'] = get_ds_id_by_code(ds_code)
    data['dataSourceCode'] = data_source['code']
    data['name'] = data_source['name']
    data['description'] = data_source['description']
    data['type'] = 'vnext'
    data['connectionCount'] = data_source['connectionCount']
    data['hasWidgetGallery'] = True
    data['orderNumber'] = 100
    data['tableCount'] = None
    data['templetLevel'] = 'report_level'
    data['code'] = ds_code
    return data
