# -*- coding: utf-8 -*-

from restart.resource import Resource


ACTION_MAP = {
    'POST': 'post',
    'GET': 'get',
    'PUT': 'put',
    'PATCH': 'patch',
    'DELETE': 'delete',
    'OPTIONS': 'options',
    'HEAD': 'head',
    'TRACE': 'trace'
}


class Interface(Resource):
    """The class that represents a non-REST resource, which is a
    traditional HTTP interface.
    """

    def __init__(self, action_map=None):
        super(Interface, self).__init__(ACTION_MAP)
