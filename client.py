import poll
import time
import msgpack
import socket
import nacl.public as nacl
from llog import msgpack_hook


class Client:
    def __init__(self, rperiod=15, host='localhost', port=6444, iface=None, **poller_kwargs):
        """Constructor for client.
        rperiod - the approximate time interval in minutes between successive reports to server.
        host
        port
        poller_kwargs - keyword arguments supplied to the poller. See poll.Poller for more info.
        """

        assert rperiod != 0

        self.target = (host, port)
        self.poller = poll.Poller(**poller_kwargs)
        self.poller.start()
        self.sniff = poll.Sniffer(iface)
        self.rperiod = rperiod
        self.et_report = rperiod

    def send_report(self):
        """Connect to server and send all pending logs."""

        # Collect logs
        total_logs = []
        total_logs.extend(self.poller.log_queue)
        l = len(total_logs)
        self.poller.log_queue[:l] = []
        total_logs.extend(self.sniff.log_queue)
        self.sniff.log_queue[:len(total_logs)-l] = []
        print(*total_logs, sep='\n')

        # Connect and send.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.target)
        klen = int.from_bytes(sock.recv(1))  # Key length
        if klen == 0:  # No Key
            print("warning: connection to server is not encrypted.")
            filelike = sock.makefile(mode='wb')
            msgpack.pack(total_logs, filelike,
                         default=msgpack_hook, use_bin_type=True)
            filelike.close()
        else:
            # Read key data
            key_data = sock.recv(klen)
            pkey = nacl.PublicKey(
                key_data, encoder=nacl.encoding.RawEncoder)  # Construct key
            sealed_box = nacl.SealedBox(pkey)
            enc_data = sealed_box.encrypt(msgpack.packb(total_logs,
                                                        default=msgpack_hook, use_bin_type=True))    # Serialize and encrypt.
            # Send data length as 4 bytes.
            sock.sendall(len(enc_data).to_bytes(4))
            sock.sendall(enc_data)
        sock.close()

    def begin(self):
        """Start client."""
        while True:
            print("Monitoring... ")
            self.send_report()
            time.sleep(self.rperiod)
