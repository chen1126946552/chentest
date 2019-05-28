'''Decorator for user token verification'''

from __future__ import absolute_import
from http import HTTPStatus
import logging
from functools import wraps

from flask import current_app as flask_app, request
from common.http.utils import get_json
from common.service.response import make_error_response


logger = logging.getLogger(__name__)


SKIP_VERIFY_URLS =\
    [
        "/pt/users/goSignin",
        "/api/v2/users/signin",
        "/api/v2/users/activation",
        "/pt/users/ga/signin",
        "/pt/users/signout",
        "/api/v1/users/sg/signin",
        "/pt/ptengine/auth",
        "/pt/ptengine/authConfirm",
        "/pt/users/signin",
        "/pt/users/signup",
        "/pt/users/exists",
        "/pt/users/send",
        "/pt/users/verifyResetPasswordRequest",
        "/pt/users/getPassword",
        "/pt/users/password/reset",
        "/pt/users/getAccessToken",
        "/pt/users/shareSignin",
        "/pt/file/excelFileUpload",
        "/pt/file/excelFileUpdate",
        "/pt/users/updateForwardCount",
        "/pt/test",
        "/pt/discourse",
        "/pt/space/invite/",
        "/pt/space/checkInviteUrl/",
        "/pt/space/acceptInvite/",
        "/api/v2/spaces/acceptInvite/",
        "/pt/space/checkDomain/",
        "/pt/file/imgUpload",
        "/api/v2/file/imgUpload",
        "/pt/users/pte/",
        "/pt/panels/share/verification",
        "/pt/users/pte/",
        "/pt/ptengine/heatmap/data",
        "/api/v2/spaces/checkInviteUrl/",
        "/api/v1/datasources/config/common",
        "/api/v1/users/password/reset",
        "/api/v2/users/signinValidate",
        "/api/v2/users/ptsso",
        "/api/v2/users/token",
        "/api/v2/users/ptelogin",
        "/api/v2/spaces/nosession",
        "/api/v2/panels/nosession",
        "/api/v2/signinwith/",
        "/api/v1/panels/share/verification",
        "/api/v1/users/forgot",
        "/api/v1/users/forgot/validate",
        "/api/v1/users/active/repeat",
        "/api/v1/users/active",
        "/api/v2/users/settings/spaceSelected",
        "/api/v1/users/password/reset/validate",
        "/api/v2/users/shareSignin/",
        "/api/v1/public/websocket/push",
        "/api/v1/public/client/info",
        "/api/v1/public/sys/params/",
        "/api/v1/public/web/log",
        "/api/v1/public/invitation-code/generate",
        "/api/v1/public/invitation-code/exists",
        "/api/v1/public/sys/config/i18n/",
        "/api/v1/websocket/|/validate",
        "/api/v2/panels/verifyDashboardAccess",
        "/api/v3/ds/etl/dataset/datasource/|/data",
        "/api/v1/widgets/dataset/refresh/",
        "/api/v1/connections/config/",
        # accessToken path
        "/pt/users/shareUserInfo/",
        "/pt/panels/getPanel/",
        "/pt/widgets/widgetWithLayout/",
        "/pt/widgets/widget/",
        "/pt/data/widgetData/",
        "/pt/data/batchWidgetData/",
        "/pt/widgets/getOne/",
        "/api/v1/panels",
        "/api/v1/widgets/batchWidgetData/",
        "/api/v2/spaces/",
        "/api/v1/commands/fieldval",
        "/api/v1/commands/panels/filters/fieldValue",
        "/api/v2/widgets/base",
        "/api/v1/widgets/"
    ]

SKIP_VERIFY_ADVANCED_URLS = \
[
    ("/api/v1/websocket", "validate"),
    ("/api/v3/ds/etl/dataset/datasource/", "data"),
    ("/api/v1/widgets/", "data/temp"),
    ("/api/v1/widgets/", "datasources/configurations"),
    ("/api/v1/widgets/", "data"),
    ("/api/v1/datasources/", "filter/fields"),
    ("/api/v1/panels/", "profiles"),
]

def _do_verify_token(req):
    if 'Token' not in req.headers:
        return False

    #TODO: verify UID/SpaceId headers match token

    token_validation_url = f'{flask_app.config["MIDDLE_URL"]}/api/v2/users/signinValidate'
    body = get_json(token_validation_url, headers={'Token': req.headers['Token']})
    return body and 'success' in body and body['success'] is True


def _is_verify_need(req):
    url = req.path
    if any([x for x in SKIP_VERIFY_URLS if url.startswith(x)]) or \
        any([x for x in SKIP_VERIFY_ADVANCED_URLS if url.startswith(x[0]) and url.endswith(x[1])]):
        return False

    return True

def verify_token(func):
    '''
    Decorator for verifying token in request. If verification failed, HTTP 401 response
    is returned.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            if _is_verify_need(request) and not _do_verify_token(request):
                logger.warning('Request failed token verification: %s %s',
                               request.method, request.path)
                return make_error_response('Invalid token', HTTPStatus.UNAUTHORIZED)
        return func(*args, **kwargs)
    return wrapper
