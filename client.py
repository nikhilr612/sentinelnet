import poll
import time
import msgpack
import socket
from llog import msgpack_hook, msgupack_hook


class Client:
    def __init__(self, rperiod=15, host='localhost', port=6444, **poller_kwargs):
        """
        Constructor for client.
        rperiod - the approximate time interval in minutes between successive reports to server.
        host
        port
        poller_kwargs - keyword arguments supplied to the poller. See poll.Poller for more info.
        """

        assert rperiod != 0

        self.target = (host, port)
        self.poller = poll.Poller(**poller_kwargs)
        self.poller.start()
        self.sniff = poll.Sniffer()
        self.rperiod = rperiod
        self.et_report = rperiod

    def send_report(self):
        """
        Connect to server and send all pending logs.
        """
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
        filelike = sock.makefile(mode='wb')
        msgpack.pack(total_logs, filelike,
                     default=msgpack_hook, use_bin_type=True)
        filelike.close()
        sock.close()

    def begin(self):
        """
        Start client.
        """
        while True:
            print("Monitoring... ")
            self.send_report()
            time.sleep(self.rperiod)
