# -*- coding: utf-8 -*-
import time
import json

from django.conf import settings
from django.http import HttpResponse


def http_response(request, context={}, statuscode=None, code=None, msg=None, content_type=None):
    """
    统一的http response封装，增加通用返回参数，返回值为HttpResponse对象

    默认情况下，output为json时返回content-type为application/json, jsonp时返回content-type为application/javascript,
    可以通用content_type改变content-type的默认行为

    :param request: django请求对象
    :param context: 响应数据字典 type:dict
    :param statuscode: 错误状态对象
    :param code: 自定义错误码，为空则使用`statuscode`的错误码
    :param msg: 自定义错误信息，为空则使用`statuscode`的msg
    :param result: 响应结果状态，默认为None，自动判断 type: bool

    :return str 序列化json数据或pb流
    """
    content_dict = {
        "version": settings.VERSION,
        "code": code if code is not None else statuscode.code,
        "msg": msg if msg is not None else statuscode.msg,
        "msg_cn": getattr(statuscode, 'msgcn', ''),
        "timestamp": int(time.time()),
    }
    content_dict.update(context)
    response_content = json.dumps(content_dict)
    output = request.parameters.get('output', 'json')
    # 根据不同的output类型返回不同的结果
    if output == 'jsonp':
        callback = request.parameters.get('callback', 'callback')
        response_content = '{0}({1});'.format(callback, response_content)
        content_type = content_type or 'application/javascript'
        return HttpResponse(response_content, content_type=content_type)
    else:
        content_type = content_type or 'application/json'
        return HttpResponse(response_content, content_type=content_type)
