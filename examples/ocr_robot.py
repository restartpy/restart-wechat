# -*- coding: utf-8 -*-

"""OCR（Optical Character Recognition，光学字符识别）机器人

环境搭建（On Ubuntu）：

    $ sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install pytesseract
    $ pip install requests
    $ pip install pillow
    $ pip install restart-wechat
"""

from cStringIO import StringIO

import pytesseract
import requests
from PIL import Image
from restart.api import RESTArt
from restart.ext.wechat.wechat import WeChat

api = RESTArt()


@api.route(uri='/YOUR_URL')
class OCRRobot(WeChat):
    token = 'YOUR_TOKEN'
    encoding_aes_key = 'YOUR_ENCODING_AES_KEY'
    app_id = 'YOUR_APP_ID'

    def on_image(self, message):
        image_url = message.image
        image = Image.open(StringIO(requests.get(image_url).content))
	text = pytesseract.image_to_string(image, lang='chi_sim')
        return text
