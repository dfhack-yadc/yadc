# Communication
# TODO: Rewrite to use a better library

import select, socket, threading

import yadc.util as util

# From C++
YADC_MSG_OK = 0
YADC_MSG_ERROR = 1
YADC_ERR_ID_IN_USE = 1
def encode_error(code):
    return chr(YADC_MSG_ERROR) + chr(code)

class ServerConnectionHandler(threading.Thread):
    def __init__(self, server):
        super(ServerConnectionHandler, self).__init__()
        self.server = server

    def run(self):
        server = self.server
        while True:
            try:
                r, w, e = select.select([server.socket], [], [])
                if len(r):
                    server.add_client(server.connection_class(*server.socket.accept()))
                else:
                    raise select.error
            except select.error:
                break

class ServerConnection(object):
    def __init__(self, conn, addr):
        self.socket, self.addr = conn, addr

    def __repr__(self):
        return '<%s: %s:%s>' % ((self.__class__.__name__, ) + self.addr)

class Server(object):
    handler_class = ServerConnectionHandler
    connection_class = ServerConnection
    def __init__(self, addr='0.0.0.0', port=8000):
        self.handler = self.handler_class(self)
        self.lock = threading.RLock()
        self.clients = []
        self.addr, self.port = addr, port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((addr, port))

    def __repr__(self):
        return '<%s: %s:%s>' % (self.__class__.__name__, self.addr, self.port)

    def add_client(self, client):
        with self.lock:
            self.clients.append(client)
            util.log('New client: ' + repr(client))

    def remove_client(self, client):
        if isinstance(client, int):
            client = self.clients[client]
        client_id = self.clients.index(client)
        with self.lock:
            try:
                client.socket.close()
            except socket.error:
                pass
            util.log('Client disconnected: ' + repr(client))
            self.clients[client_id] = None

    def get_active_sockets(self):
        """ Return a list of all active (i.e. not None) sockets """
        return [c.socket for c in self.clients if c is not None]

    def listen(self):
        util.log('server listening on %s:%i' % (self.addr, self.port))
        self.socket.listen(4)
        self.handler.start()

    def shutdown(self, silent=False):
        try:
            self.socket.close()
        except socket.error:
            if not silent:
                raise


class ScreenServerConnection(ServerConnection):
    def __init__(self, conn, addr):
        super(ScreenServerConnection, self).__init__(conn, addr)

class ScreenServer(Server):
    connection_class = ScreenServerConnection

class CommServerConnection(ServerConnection):
    pass

class CommServer(Server):
    connection_class = CommServerConnection
