import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        loader = tornado.template.Loader(".")
        print 'here'
        # self.write(loader.load("client_interface/home.html").generate())
        self.write('shitye')


class WSHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print 'connection opened...'
        self.write_message(
            "The server says: 'Hello'. Connection was accepted.")

    def on_message(self, message):
        self.write_message("The server says: " + message + " back at you")
        print 'received:', message

    def on_close(self):
        print 'connection closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
  # (r'/home', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
