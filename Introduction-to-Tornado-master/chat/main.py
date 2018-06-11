# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.httpclient
import os
import datetime

from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
import json
define("port", default=8000, type=int)

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")

class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器

    def open(self):
        self.users.add(self)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        for u in self.users:  # 向在线用户广播消息
            u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        for u in self.users:
            u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


class getPosHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous  # 不关闭连接，也不发送响应
    def post(self):
        http = tornado.httpclient.AsyncHTTPClient()
        # ip = self.request.remote_ip
        ip = '122.226.73.28'
        http.fetch("http://ip.taobao.com/service/getIpInfo.php?ip={}".format(ip),
                   callback=self.on_response)

    def on_response(self, response):
        if response.error:
            print(response.error)
            self.send_error(500)
        else:
            data = json.loads(response.body)
            # self.set_header('Content-Type','application/json;charset=UTF-8')
            if 0 == data["code"]:
                self.write(u"省份: %s 城市: %s" % (data['data']["region"], data['data']["city"]))
            else:
                self.write("查询IP信息错误")
        self.finish() # 发送响应信息，结束请求处理

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/chat", ChatHandler),
			(r'/getpos',getPosHandler),
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True,
		xsrf_cookies=False,
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()