import tornado.ioloop
import tornado.web
# import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class StatusHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        self.write({ 'hello': 'world' })

def make_app():
    return tornado.web.Application([
        (r"/helloworld", MainHandler),
        (r"/status", StatusHandler),
        (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': './static/css'}),
        (r'/page/(.*)', tornado.web.StaticFileHandler, {'path': './static/page'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path': './static/page', "default_filename": "index.html"}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
