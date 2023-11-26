import msgpack
import socket
from threading import Thread
from llog import msgupack_hook
from collections.abc import Callable

def servlet_action(conn):
    """
    Target function for servlet threads.
    """
    reader = conn.makefile(mode='rb')
    data = msgpack.unpack(reader, ext_hook=msgupack_hook)
    print(data)
    reader.close()
    conn.close()

class Server(Thread):
    def __init__(self, port: int = 6444, queue: int = 5, target: Callable[[socket.socket], None] = servlet_action):
        """
        Create a socket and bind to a specific port, with a maximum number of connections to enqueue.
        """
        assert port != 0
        assert queue != 0

        Thread.__init__(self)

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(('', port))
        self.target = target
        self.conn_queue = queue
        self.alive = True

    def kill(self):
        """
        Terminate the server loop.
        """
        self.alive = False

    def run(self):
        self.serversocket.listen(self.conn_queue)
        while self.alive:
            conn, addr = self.serversocket.accept()
            print("Accepted connection from", addr)
            sthread = Thread(target=self.target, args=(conn,))
            sthread.start()


if __name__ == "__main__":
    s = Server()
    s.start()
