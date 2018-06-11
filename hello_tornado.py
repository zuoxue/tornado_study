#！-*-coding:utf-8-*-
import tornado.web,tornado.ioloop,tornado.httpserver,tornado.options

from tornado.options import define,options
from tornado.web import url
import json

define('port',default=8000,type=int,help='port default value')


class IndexHandler(tornado.web.RequestHandler):
	# def initialize(self,index):
	# self.index = index

	def get(self,date,subject):
		# print(self.reverse_url('index'))
		obj={
			'name':'wanghai',
			'sex':'male',
			'data':self.request.method
		}
		self.write(u'hello,tornado,meimei<br/>')
		self.write(u'date:'+date+u'<br/>')
		self.write(u'subject:'+subject+u'<br/>')
		self.write(json.dumps(obj))
		self.set_header('itast','sdsds')
		self.set_status(211,'sds sdfs')
		self.send_error(211,contend="未发现页面")

	def write_error(self,status_code,**kwargs):
		self.write(u"<h1>页面奔溃了，程序员gg正在赶过来</h1>")
		self.write('<p>%s</p>'%kwargs.get("contend"))

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application([
			url(r'/(?P<subject>[a-zA-Z]+)/(?P<date>\d+)/',IndexHandler,name='index'),
		])
	http_server = tornado.httpserver.HTTPServer(app)
	print(options.ports)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()