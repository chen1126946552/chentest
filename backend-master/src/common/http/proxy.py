'''
Utility module for proxying an incoming Flask request to a downstream service.
'''

from __future__ import absolute_import
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

from flask import Response

from .utils import get_session


#File upload param name
FILE_PARAM_NAME = 'file'

def proxy_raw(request, new_url):
    '''
    Proxies a flask request to the new url and returns its raw response to the caller.

    :param request: The original flask request.
    :param new_url: The URL to which the request should be proxied.
    :returns: Response object of requests.request(...) call
    '''

    if request.args:
        parts = list(urlparse(new_url))
        query = parse_qs(parts[4])
        query.update({(k, v) for k, v in request.args.items()})
        parts[4] = urlencode(query, doseq=True)
        new_url = urlunparse(parts)

    headers = {key: value for (key, value) in request.headers if key != 'Host'}

    files = None
    if request.files:
        file = request.files.get(FILE_PARAM_NAME, None)
        if file:
            # Requests library will generate it itself
            del headers['Content-Type']
            files = {FILE_PARAM_NAME: (file.filename, file, file.content_type, file.headers)}

    resp = get_session().request(
        method=request.method,
        url=new_url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        files=files,
        allow_redirects=False)

    return resp


def proxy(request, new_url):
    '''
    Proxies a flask request to the new url and returns response as Flask response to the caller.

    :param request: The original flask request.
    :param new_url: The URL to which the request should be proxied.
    :returns: Http response wrapped into a Flask Response object.
    '''
    resp = proxy_raw(request, new_url)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response
