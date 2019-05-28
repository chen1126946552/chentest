"""Space service"""
from __future__ import absolute_import
import logging
from services.connection_service import Connection as csvc
from services import access_rule_service
# pylint: disable=no-member

logger = logging.getLogger(__name__)


def transfer_resources(old_uid, new_uid, space_id):
    """
    Removes a space member and transfers resources
    Args:
        old_uid: Remove member user id
        new_uid: Transfer to user id
        space_id: Space id
    """
    logging.info("Transfer resources start,old_uid[%s],new_uid[%s],space_id[%s]",
                 old_uid,
                 new_uid,
                 space_id)
    csvc.transfer_connections(old_uid, new_uid, space_id)
    logging.info("Transfer connections user[%s] to [%s] successful", old_uid, new_uid)
    access_rule_service.transfer_ownership(old_uid, new_uid, space_id)
    logging.info("Transfer access rule user[%s] to [%s] successful", old_uid, new_uid)
