#!coding:utf8

import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver

from tornado.options import options,define
define("port",default=8080,help="define a port",type=int)

class IndexHamdler(tornado.web.RequestHandler):
    """
        define a initial page =汪海
    """
    def get(self):
        self.write("hello,world")

    def write_error(self,status_code,**kwargs):
        self.write("you get a %d error"%status_code)
tornado.options.parse_command_line()
app = tornado.web.Application(handlers=[(r'/',IndexHamdler)])
http_server = tornado.httpserver.HTTPServer(app)
http_server.listen(options.port)
tornado.ioloop.IOLoop.instance().start()
