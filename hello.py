# import tornado.httpserver
# import tornado.ioloop
# import tornado.options
# import tornado.web
# from tornado.options import define, options
# define("port", default=8000, help="run on the given port", type=int)
# class IndexHandler(tornado.web.RequestHandler):
#     def get(self):
#         greeting = self.get_argument('greeting', 'Hello')
#         self.write(greeting + ', friendly user!')
# if __name__ == "__main__":
#     tornado.options.parse_command_line()
#     app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
#     http_server = tornado.httpserver.HTTPServer(app)
#     http_server.listen(options.port)
#     tornado.ioloop.IOLoop.instance().start()

#coding=utf-8
import logging
import logging.handlers
import sys
reload(sys)
sys.setdefaultencoding('utf8')

LOG_FILE = 'D://tst.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('tst')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info('first info message')
logger.debug('first debug message')
