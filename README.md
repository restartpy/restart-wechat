# RESTArt-Wechat

A RESTArt extension for Wechat Media Platform development.

用于微信公众平台开发的 [RESTArt][1] 扩展库。


## 安装

目前只有开发版本:

```
$ pip install -e git+https://github.com/RussellLuo/restart-wechat.git#egg=restart-wechat
```


## 快速入门

### 服务端实现

一个自动回复微信文本消息的简单机器人:

```python

# robot.py

from restart.api import RESTArt
from restart.ext.wechat.wechat import Wechat

api = RESTArt()

@api.route(uri='/YOUR_URL')
class Robot(Wechat):
    token = 'YOUR_TOKEN'
    encoding_aes_key = 'YOUR_ENCODING_AES_KEY'
    app_id = 'YOUR_APP_ID'

    def on_text(self, message):
        return u'你说：%s' % message.content

```

启动本地服务:

```
$ restart robot:api
```

借助 [Ngrok][2] 将本地服务（侦听在 5000 端口）对外开放：

```
$ ./ngrok http 5000

ngrok by @inconshreveable

Tunnel Status                 online
Version                       2.0.19/2.0.19
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://0d187fdb.ngrok.io -> localhost:5000
Forwarding                    https://0d187fdb.ngrok.io -> localhost:5000
```

其中，`http://0d187fdb.ngrok.io` 就是可以访问本地服务的外网地址。

### 公众平台配置

进入微信公众平台官网，申请一个 [测试号][3]。

申请成功后，系统会自动为你生成一个应用ID：

```
AppID(应用ID): YOUR_APP_ID (自动生成)
```

紧接着，配置服务器如下:

```
URL(服务器地址): http://0d187fdb.ngrok.io/YOUR_URL
Token(令牌): YOUR_TOKEN
EncodingAESKey(消息加解密密钥): YOUR_ENCODING_AES_KEY (随机生成)
```

**注意**：上面的 `YOUR_APP_ID`、`YOUR_URL`、`YOUR_TOKEN` 和 `YOUR_ENCODING_AES_KEY`（只有正式的订阅号和服务号才有 `消息加解密密钥`，测试号没有），必须与服务端代码中的配置一致。

### 微信测试

用微信扫描“测试号二维码”，然后给测试号发送文本消息，并查看回复。


## 更多示例

查看 [examples][4]。


## License

[MIT][5]


[1]: https://github.com/RussellLuo/restart
[2]: https://ngrok.com
[3]: http://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
[4]: https://github.com/RussellLuo/restart-wechat/tree/master/examples
[5]: http://opensource.org/licenses/MIT
