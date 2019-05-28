import sys
import os

import yaml
from jsonpath import jsonpath

sys.path.append(os.path.join(os.path.dirname(__file__), '../main'))

from services.adaptors.datasource_config import ds_config_adapt


def test_ds_config_adapt():
    with open(os.path.join(os.path.dirname(__file__), 'googleanalytics-v4.yml'), 'r') as f:
        config = yaml.load(f)

    adapted = ds_config_adapt('googleanalytics-v4', config, 'en_US')
    assert jsonpath(adapted, '$.config.basicInfo.isSupportCalculatedField')[0] is True
    assert jsonpath(adapted, '$.config.basicInfo.isSupportI18n')[0] is True

    assert jsonpath(adapted, '$.config.datasource.commands[0].id')[0] == 'profile'
    assert jsonpath(adapted, '$.config.datasource.view.steps[*].type') == ['account', 'profile']

    assert jsonpath(adapted, '$.config.widgetEditor.map.mapType[*].code') == ['world', 'country']
    assert len(jsonpath(adapted, '$.config.widgetEditor.graphs[*]')) == 14
    assert jsonpath(adapted, '$.config.widgetEditor.time.default')[0] == 'past'
    assert len(jsonpath(adapted, '$.config.widgetEditor.time.items[*]')) == 16
    assert jsonpath(adapted, '$.config.widgetEditor.time.isSupportSelectDateFields') is False
    assert len(jsonpath(adapted, '$.config.widgetEditor.segment.operations.items[*]')) == 2
    assert len(jsonpath(adapted, '$.config.widgetEditor.segment.operators.string.items[*]')) == 6
    assert len(jsonpath(adapted, '$.config.widgetEditor.segment.operators.number.items[*]')) == 6
    assert len(jsonpath(adapted, '$.config.widgetEditor.segment.scopes.items[*]')) == 2
    assert len(jsonpath(adapted, '$.config.widgetEditor.filter.commands[*]')) == 1
    assert len(jsonpath(adapted, '$.config.widgetEditor.filter.string.options[*]')) == 2
    assert len(jsonpath(adapted, '$.config.widgetEditor.filter.string.options[1].items[*]')) == 6
