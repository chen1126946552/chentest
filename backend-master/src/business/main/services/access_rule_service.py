"""Access rule service"""
from __future__ import absolute_import
import logging
from app import db
from models.access_rule import AccessRule as AccessRuleModel
# pylint: disable=no-member

logger = logging.getLogger(__name__)


def create(**kwargs):
    """
    Create access rule
    Args:
        data: AccessRule object
    Returns: AccessRule
    """
    arm = AccessRuleModel(**kwargs)
    AccessRuleModel.insert(arm)
    return arm


def get_by_space_resource_type(space_id, resource_type):
    """
    Query by spaceId and resourceType
    Args:
        space_id: User's space id
        resource_type: Access resource type

    Returns:
        access rule list
    """
    return AccessRuleModel.query.filter_by(
        space_id=space_id,
        resource_type=resource_type).all()


def delete_by_id(id):
    """Delete access rule by id"""
    AccessRuleModel.delete_by_id(id)


def delete_by_all(**kwargs):
    """
    Delete by resource_id,resource_type,space_id
        resource_id: (required) Access resource id
        resource_type: (required) Access resource type
        space_id: (required) User's space id
        owner_id: (optional) Resource owner id
        user_id: (optional Resource sharer id
        group_id: (optional) group id
    """
    resource_id = kwargs["resource_id"]
    resource_type = kwargs["resource_type"]
    space_id = kwargs["space_id"]
    owner_id = kwargs.get("owner_id")
    user_id = kwargs.get("user_id")
    group_id = kwargs.get("group_id")

    access_rule_list = _query_by_all(resource_id, resource_type, space_id,
                                     owner_id, user_id, group_id)
    for access_rule in access_rule_list:
        access_rule.delete()


def update_access_level(**kwargs):
    """
    Update access level
        resource_id: (required)  Access resource id
        resource_type: (required) Access resource type
        space_id: (required) User's space id
        access_level: (required) Access level
        owner_id: (optional) Resource owner id
        user_id: (optional) Resource sharer id
        group_id: (optional) group id
    """
    resource_id = kwargs["resource_id"]
    resource_type = kwargs["resource_type"]
    space_id = kwargs["space_id"]
    access_level = kwargs["access_level"]
    owner_id = kwargs.get("owner_id")
    user_id = kwargs.get("user_id")
    group_id = kwargs.get("group_id")

    access_rule_list = _query_by_all(resource_id, resource_type, space_id,
                                     owner_id, user_id, group_id)
    for access_rule in access_rule_list:
        access_rule.access_level = access_level
    db.session.commit()


# pylint: disable=too-many-arguments
def _query_by_all(resource_id, resource_type, space_id,
                  owner_id=None, user_id=None, group_id=None):
    query_params = {
        "space_id": space_id,
        "resource_type": resource_type,
        "resource_id": resource_id
    }
    if owner_id:
        query_params["owner_id"] = owner_id
    if user_id:
        query_params["user_id"] = user_id
    if group_id:
        query_params["group_id"] = group_id

    return AccessRuleModel.query.filter_by(**query_params).all()


def transfer_ownership(old_uid, new_uid, space_id):
    """
     Removes a space member and transfers shared access rule owner id
    Args:
        old_uid: Remove user id
        new_uid: Transfer to new user id
        space_id: Space id
    """
    access_rule_list = AccessRuleModel.query.filter_by(
        space_id=space_id
    ).all()
    for rule in access_rule_list:
        if rule.owner_id == old_uid:
            rule.owner_id = new_uid
        if rule.user_id == old_uid:
            rule.user_id = new_uid
        if rule.user_id == rule.owner_id:
            rule.delete()
    db.session.commit()

    # Clean the duplicated access rule records after transfer the
    # share-user permission based on weight
    # a --> b   1)  edit
    # a --> c   2)  read
    # after c transfer share to b
    # a --> b   1)  edit
    # a --> b   2)  read ::need to delete
    new_access_rule_list = AccessRuleModel.query.filter_by(
        space_id=space_id,
        user_id=new_uid
    ).all()
    exist_access_dict = {}
    delete_access_list = []
    for access_rule in new_access_rule_list:
        # In designated space and user, resource id plus owner_id
        # uniquely determined one share
        res_key = str(access_rule.owner_id) + str(access_rule.resource_id)
        if res_key in exist_access_dict:
            exist_rule = exist_access_dict.get(res_key)
            if access_rule.get_access_level_weight() > exist_rule.get_access_level_weight():
                delete_access_list.append(exist_rule)
                exist_access_dict[res_key] = access_rule
            else:
                delete_access_list.append(access_rule)
        else:
            exist_access_dict[res_key] = access_rule
    for r in delete_access_list:
        r.delete()
    db.session.commit()
