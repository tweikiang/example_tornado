import tornado.ioloop
import tornado.web
import sqlite3
from sqlite3 import Error

port = 8888
dbfile = 'example.db'
conn = None
try:
    conn = sqlite3.connect(dbfile)
    print(sqlite3.version)
except Error as e:
    print(e)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        self.write(body)
    def delete(self):
        self.write("Logout")

class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        if conn:
            try:
                c = conn.cursor()
                c.execute("SELECT users FROM sqlite_temp_master WHERE type='table';")
                print(c.fetchall())
                self.write(body)
            except Error as e:
                print(e)
                # create table if not exists table_name (column1, column2, …, columnN)
                self.write(body)
        else:
            self.set_status(503, "errorConnectToDB")

class StatusHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        self.write({ 'hello': 'world' })

def make_app():
    return tornado.web.Application([
        (r"/helloworld", MainHandler),
        (r"/status", StatusHandler),
        (r"/api/login", LoginHandler),
        (r"/api/register", RegisterHandler),
        (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': './static/css'}),
        (r'/page/(.*)', tornado.web.StaticFileHandler, {'path': './static/page'}),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path': './static/page', "default_filename": "index.html"}),
    ])

if __name__ == "__main__":
    # create_connection(dbfile)
    app = make_app()
    app.listen(port)
    print('web server is started @ http://localhost:' + str(port))
    # tornado.ioloop.IOLoop.current().start()
    # signal : CTRL + BREAK on windows or CTRL + C on linux
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
    finally:
        if conn:
            conn.close()
