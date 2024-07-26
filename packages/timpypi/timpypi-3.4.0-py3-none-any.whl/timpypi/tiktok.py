
# -*- coding: utf-8 -*-
# 1 : imports of python lib
import hashlib
import hmac
from datetime import datetime
from requests import Request, Response
from timpypi.utils import exception


@exception
def request(method, domain, api, headers, body, params, ttype) -> Response:
    """ Custom request special for TikTok API
    :param Request method: one of `get`, `post`, `put`, `patch`, `delete`
    :param str domain: one of `https://auth.tiktok-shops.com` or ```https://open-api.tiktokglobalshop.com```
    :param str api: api special for request. example: `/authorization/202309/shops`
    :param dict headers: header for request.
    :param dict body:
    :param dict params: query
    :param str ttype: `data` or `json`
    :return: Response
    """
    if "timestamp" not in params.keys():
        params["timestamp"] = str(int(datetime.timestamp(datetime.now())))
    pairs = [f"{key}={value}" for key, value in params.items()]
    url = domain + api + "?" + "&".join(pairs)
    if ttype == "json":
        return method(url, params=params, headers=headers, json=body)
    return method(url, params=params, headers=headers, data=body)
