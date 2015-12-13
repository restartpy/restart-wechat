# -*- coding: utf-8 -*-

from restart.parsers import Parser
from restart.renderers import Renderer
from restart.exceptions import Forbidden, NotImplemented, BadRequest
from wechatpy import parse_message, create_reply
from wechatpy.crypto import WeChatCrypto
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException
)

from .interface import Interface
from .config import config


class CheckSignatureMiddleware(object):
    """The middleware class for checking signature."""

    def process_request(self, request):
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        try:
            check_signature(config.TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            raise Forbidden()


class XMLParser(Parser):
    """The XML parser class for messages."""

    content_type = 'text/xml'

    def parse(self, stream, content_type, content_length, context=None):
        data = stream.read()

        request = context['request']
        encrypt_type = request.args.get('encrypt_type', 'raw')
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        # In encryption mode
        if encrypt_type != 'raw':
            crypto = WeChatCrypto(config.TOKEN, config.ENCODING_AES_KEY,
                                  config.APP_ID)
            try:
                data = crypto.decrypt_message(data, msg_signature,
                                              timestamp, nonce)
            except (InvalidSignatureException, InvalidAppIdException):
                raise BadRequest()

        msg = parse_message(data)
        return msg


class XMLRenderer(Renderer):
    """The XML renderer class for replies."""

    content_type = 'text/xml'
    format_suffix = 'xml'

    def render(self, data, context=None):
        request = context['request']
        encrypt_type = request.args.get('encrypt_type', 'raw')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        # In encryption mode
        if encrypt_type != 'raw':
            crypto = WeChatCrypto(config.TOKEN, config.ENCODING_AES_KEY,
                                  config.APP_ID)
            data = crypto.encrypt_message(data, nonce, timestamp)

        return data


class Wechat(Interface):
    """The class that represents a Wechat interface."""

    #: The Wechat configuration
    token = None
    encoding_aes_key = None
    app_id = None

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

    #: The resource-level middleware classes
    middleware_classes = (CheckSignatureMiddleware,)

    def __init__(self, action_map):
        # Assure that the configuration is loaded
        self.load_config()
        super(Wechat, self).__init__(action_map)

    @classmethod
    def load_config(cls):
        if not getattr(cls, '_has_loaded', False):
            config.TOKEN = cls.token
            config.ENCODING_AES_KEY = cls.encoding_aes_key
            config.APP_ID = cls.app_id

            cls._has_loaded = True

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
