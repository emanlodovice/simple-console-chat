import json

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

clients = []


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        loader = tornado.template.Loader(".")
        print 'here'
        self.write(loader.load("client_interface/home.html").generate())


class WSHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print 'connection opened...'
        clients.append(self)
        self.write_message('Connected')

    def on_message(self, message):
        message = json.loads(message)
        msg_string = '{} said: {}'.format(
            message['username'], message['message'])
        for client in clients:
            client.write_message(msg_string)

    def on_close(self):
        print 'connection closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
    ip = raw_input('ip > ')
    application.listen(5000, address=ip)
    tornado.ioloop.IOLoop.instance().start()
