import msgpack
import socket
from threading import Thread
from llog import msgupack_hook
from collections.abc import Callable
import nacl.public as nacl
import scapy.layers.l2 as scapy_l2

# Type hint for servlet action callback.
# First parameter is an identifier for the connection.
# Second parameter is the list of logs received.
Callback_t = Callable[[str, list[tuple]], None];

def _raw_base(ip_addr: str, conn: socket.socket, func: Callback_t):
    """
    Target function for servlet threads that calls func with the logs as argument.
    Communication is not encrypted in any manner.
    """
    conn.send(b'\x00');     # Indicate to client that connection is un-encrypted.
    reader = conn.makefile(mode='rb');
    data = msgpack.unpack(reader, ext_hook=msgupack_hook);
    func(scapy_l2.getmacbyip(ip_addr), data);
    reader.close();
    conn.close();

def _ecc_base(ip_addr: str, conn: socket.socket, func: Callback_t):
    """
    Target function for servlet threads that calls func wiht logs as argument.
    Communication is through ECurve25519 encryption.
    """

    skey = nacl.PrivateKey.generate();                          # Ephemeral key
    key_data = skey.public_key.encode(encoder=nacl.encoding.RawEncoder); 
    conn.sendall(len(key_data).to_bytes(1));                    # Send non-zero length value
    conn.sendall(key_data);                                     # Send key.
    unseal_box = nacl.SealedBox(skey);
    data_len = int.from_bytes(conn.recv(4));                    # ..
    raw_data = unseal_box.decrypt(conn.recv(data_len));         # TODO Better way?
    data = msgpack.unpackb(raw_data, ext_hook=msgupack_hook);
    func(scapy_l2.getmacbyip(ip_addr), data);
    conn.close();

# Default action is to just dump data.
# Explicitly configure during instantiation.
# INFO Change to _ecc_enc_base for encryption.
servlet_action = _ecc_base;

class Server(Thread):
    def __init__(self, port: int = 6444, queue: int = 5, target: Callback_t = print):
        """Create a socket and bind to a specific port, with a maximum number of connections to enqueue."""
        assert port != 0;
        assert queue != 0;

        Thread.__init__(self);

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.serversocket.bind(('', port));
        self.target = target;
        self.conn_queue = queue;
        self.alive = True;

    def kill(self):
        """Terminate the server loop."""
        self.alive = False;

    def run(self):
        self.serversocket.listen(self.conn_queue);
        print("Server Online");
        while self.alive:
            conn, addr = self.serversocket.accept();
            print("Accepted connection from", addr);
            sthread = Thread(target=servlet_action, args=(addr[0], conn, self.target));
            sthread.start();


if __name__ == "__main__":
    s = Server();
    s.start();
