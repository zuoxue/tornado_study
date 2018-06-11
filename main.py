#！-*-coding:utf-8-*-
import tornado.web
import tornado.ioloop,tornado.httpserver,tornado.options

from tornado.options import define,options
from tornado.web import url
import json
import settings

define('port',default=settings.PORT,type=int,help='port default value')


class HomeHandler(tornado.web.RequestHandler):
    # def prepare(self):
        # if self.request.headers.get("Content-Type").startswith("application/json"):
        #     self.json_dict = json.loads(self.request.body)
        # else:
        #     self.json_dict = None

    def get(self):
    #     # if self.json.dict:
    #     #     for key, value in self.json_dict.items():
    #     #         self.write("<h3>%s</h3><p>%s</p>" % (key, value))
    #     # else:
    #     text="haige"
    #     self.render('index.html',text=text)
    #
    # def post(self):
    #     self.set_header("X-XSS-Protection", 0)
    #     text = self.get_argument('text','')
    #     if text:
    #         print(text)
    #     self.render('index.html',text=text)
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1
        self.set_secure_cookie("count", str(count))
        self.write(
            '<html><head><title>Cookie计数器</title></head>'
            '<body><h1>您已访问本页%d次。</h1>' % count +
            '</body></html>'
        )

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
            url(r'/',HomeHandler,name='home'),
			url(r'/(?P<subject>[a-zA-Z]+)/(?P<date>\d+)/',IndexHandler,name='index'),
		],**settings.settings)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()