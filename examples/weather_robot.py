# -*- coding: utf-8 -*-

import requests
from restart.api import RESTArt
from restart.ext.wechat.wechat import WeChat

api = RESTArt()

BAIDU_WEATHER_API = 'http://apistore.baidu.com/microservice/weather'


@api.route(uri='/YOUR_URL')
class WeatherRobot(WeChat):
    token = 'YOUR_TOKEN'
    encoding_aes_key = 'YOUR_ENCODING_AES_KEY'
    app_id = 'YOUR_APP_ID'

    def on_text(self, message):
        cityname = message.content.encode('utf-8')
        resp = requests.get(BAIDU_WEATHER_API, params={'cityname': cityname})
        result = resp.json()
        if result['errNum'] != 0:
            return u'请输入正确的城市名称（如：成都、北京）'
        else:
            template = (
                u'天气：{weather}\n气温：{temp}\n'
                u'最低气温：{l_tmp}\n最高气温：{h_tmp}\n'
                u'风向：{WD}\n风力：{WS}'
            )
            return template.format(**result['retData'])
