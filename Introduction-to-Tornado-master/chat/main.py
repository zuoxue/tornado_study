# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.httpclient
import os
import datetime
import redis
import StringIO
import settings
from tornado import gen
from tornado.web import RequestHandler,url
from tornado.options import define, options
from tornado.websocket import WebSocketHandler
from concurrent.futures import ThreadPoolExecutor
import json
define("port", default=8000, type=int)

def say_hello():
    return "hello"

class IndexHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        con = yield ThreadPoolExecutor(2).submit(say_hello)
        self.render("index.html",**{"con":con})


class make_app(object):
    def __init__(self):
        self.cache = redis.StrictRedis("localhost",6379)
        self.key = 'users'

    def add(self,name):
        self.cache.hset(self.key,name,"OK")

    def pop(self,name):
        self.cache.hdel(self.key,name)

    def get_all(self):
        return self.cache.hgetall(self.key)


class ChatHandler(WebSocketHandler):

    users = set()  # 用来存放在线用户的容器
    # users = make_app()

    def open(self):
        self.sessionid = self.get_secure_cookie()
        self.users.add(self.sessionid)  # 建立连接后添加用户到容器中
        for u in self.users:  # 向已在线用户发送消息
            u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        for u in self.users.get_all():  # 向在线用户广播消息
            u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        self.users.remove(self) # 用户关闭连接后从容器中移除用户
        for u in self.users:
            u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求


class DownLoadHandler(RequestHandler):
    def post(self):
        file = os.path.join(os.path.join(os.path.dirname(__file__)),'static','doc',ur'03.客户信息监控报告 v2.zip')

        # with open(file,"rb") as f:
        #     k = f.read(1024)
        #     print(k)
        #     while k:
        #         self.write(k)
        excel_stream = StringIO.StringIO()
        file_object = open(file, 'rb')
        while True:
            line = file_object.readline()
            excel_stream.write(line)
            if len(line) == 0:
                break
        file_object.close()
        self.set_header('Content-Type', 'appliction/octet-stream')
        self.set_header('Content-Disposition', u'attachment; filename={}'.format(ur'03.客户信息监控报告 v2.zip'))
        self.write(excel_stream.getvalue())
        return


class getPosHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous  # 不关闭连接，也不发送响应
    def post(self):
        http = tornado.httpclient.AsyncHTTPClient()
        # ip = self.request.remote_ip
        ip = '122.226.73.28'
        http.fetch("http://ip.taobao.com/service/getIpInfo.php?ip={}".format(ip),
                   callback=self.on_response)

    def on_response(self, response):
        print(self.get_secure_cookie('_xsrf'))
        if response.error:
            print(response.error)
            self.send_error(500)
        else:
            data = json.loads(response.body)
            # self.set_header('Content-Type','application/json;charset=UTF-8')
            if 0 == data["code"]:
                self.write({'data':u"省份: %s 城市: %s" % (data['data']["region"], data['data']["city"])})
            else:
                self.write("查询IP信息错误")
        self.finish() # 发送响应信息，结束请求处理

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/chat", ChatHandler),
			(r'/getpos',getPosHandler),
            url(r'/download',DownLoadHandler,name="download")
        ],
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        template_path = os.path.join(os.path.dirname(__file__), "template"),
        debug = True,
		xsrf_cookies=False,
        cookie_secret='NGU3ZDE5MjYyNTU1NDVlZTlhYjhiYTljMGZjM2VhNDU4YWJkOTBiODcxNTg0Y2RjYWM4NDg1M2ZhMDljMjUxMw=='
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("http://127.0.0.1:%s" % options.port)
    tornado.ioloop.IOLoop.current().start()
