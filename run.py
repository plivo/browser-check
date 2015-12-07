from mgr import app
from gevent import monkey
from socketio.server import SocketIOServer


monkey.patch_all()

PORT = 5000
HOST = '0.0.0.0'

if __name__ == '__main__':
    print 'Listening on http://%s.1:%s and on port 10843 (flash policy server)' % (HOST, PORT)
    SocketIOServer((HOST, PORT), app, resource="socket.io").serve_forever()
