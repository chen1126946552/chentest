"""
Utility for parsing V2 ds connection config structure.
"""


import json
from dataclasses import dataclass


@dataclass  # pylint: disable=too-many-instance-attributes
class ParsedConfig:
    """
    Class for containing fields parsed out of a V2
    ds connection config structure.
    """

    ds_connection_id: str = None
    space_id: str = None
    uid: int = None
    ds_id: int = None
    connection_id: str = None
    connection_name: str = None
    profile_path: list = None
    database_name: str = None
    table_id: str = None
    table_name: str = None


def parse(v2_ds_connection_config):
    """
    Parses a given V2 ds connection config into a `ParsedConfig`
    object.

    Args:
        v2_ds_connection_config (dict): input ds connection config.

    Returns:
        [ParsedConfig]: Parsed config object.
    """

    assert v2_ds_connection_config

    parsed = ParsedConfig()
    parsed.ds_connection_id = v2_ds_connection_config.get('dsConnectionId')
    parsed.space_id = v2_ds_connection_config.get('spaceId')
    parsed.uid = v2_ds_connection_config.get('uid')
    parsed.ds_id = v2_ds_connection_config.get('dsId')

    config = v2_ds_connection_config.get('config')
    if config:
        connection_config = config[0]
        parsed.connection_id = connection_config.get('id')
        parsed.connection_name = connection_config.get('name')

        if len(config) > 1:
            profile_config = config[1]

            # config->requestParams->id specifies the kind of ds_connection
            # whether it points to a SaaS profile or a database table
            indicator = profile_config.get('requestParams', {}).get('id')
            id_parsed = json.loads(profile_config['id'])
            assert isinstance(id_parsed, list)

            if indicator == 'table':
                assert len(id_parsed) == 2
                parsed.database_name = id_parsed[0]
                parsed.table_id = id_parsed[1]
                parsed.table_name = profile_config.get('name')
            else:
                parsed.profile_path = id_parsed

    return parsed
