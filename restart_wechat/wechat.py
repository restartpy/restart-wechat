# -*- coding: utf-8 -*-

from restart.parsers import Parser
from restart.renderers import Renderer
from restart.utils import locked_cached_classproperty
from restart.exceptions import Forbidden, NotImplemented
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from .interface import Interface


class CheckSignatureMiddleware(object):
    """The middleware class for checking signature."""

    def __init__(self, token):
        self.token = token

    def process_request(self, request):
        args = request.args
        signature = args.get('signature', '')
        timestamp = args.get('timestamp', '')
        nonce = args.get('nonce', '')

        try:
            check_signature(self.token, signature, timestamp, nonce)
        except InvalidSignatureException:
            raise Forbidden()


class XMLParser(Parser):
    """The XML parser class for messages."""

    content_type = 'text/xml'

    def parse(self, stream, content_type, content_length):
        data = stream.read()
        msg = parse_message(data)
        return msg


class XMLRenderer(Renderer):
    """The XML renderer class for replies."""

    content_type = 'text/xml'
    format_suffix = 'xml'

    def render(self, data):
        return data


class Wechat(Interface):
    """The class that represents a Webchat interface."""

    #: The token used to check signature
    token = None

    #: The message handler mapping
    handlers = {
        'text': 'on_text',
        'image': 'on_image',
        'voice': 'on_voice',
        'video': 'on_video',
        'shortvideo': 'on_shortvideo',
        'location': 'on_location',
        'link': 'on_link',
    }

    #: The parser classes used for parsing request data.
    parser_classes = (XMLParser,)

    #: The renderer classes used for rendering response data.
    renderer_classes = (XMLRenderer,)

    @locked_cached_classproperty(name='_middlewares')
    def middlewares(cls):
        return (CheckSignatureMiddleware(cls.token),)

    def message_not_handled(self, message):
        raise NotImplemented()

    def get(self, request):
        return request.args.get('echostr', '')

    def post(self, request):
        message = request.data
        handler_name = self.handlers.get(message.type, '')
        if callable(handler_name):
            handler = handler_name
        else:
            handler = getattr(self, handler_name, self.message_not_handled)
        reply = handler(message)
        result = create_reply(reply, message)
        return result.render()
