import time
import psutil
import llog
from threading import Thread
from scapy.all import IP, TCP, AsyncSniffer
from scapy.layers.http import HTTPRequest


class Poller(Thread):
    """
    An object to poll system resources and processes periodically.
    """

    def __init__(self, lfreq: int = 50, respoll_period: int = 600, procpoll_period: int = 60):
        """
        Construct a poller.
        lfreq - Number of iterations of loop per second
        respoll_period - The time in seconds between successive polls of system resources.
        sniff_period - The time in seconds between new process polls.
        """
        # Verify parameters
        assert lfreq != 0
        assert respoll_period != 0
        assert procpoll_period != 0

        Thread.__init__(self, daemon=True)

        self.res_poll_period = respoll_period
        self.proc_poll_period = procpoll_period
        self.et_res_poll = 0
        self.et_proc_poll = 0
        self.delta = 1.0/lfreq
        self.log_queue = []

    def _poll_sys_res(self):
        # Poll CPU, Memory and Disk I/O usage.
        self.log_queue.append(llog.new_line(
            llog.LogType.CPU_USAGE, psutil.cpu_percent()))
        self.log_queue.append(llog.new_line(
            llog.LogType.MEM_USAGE, psutil.virtual_memory().percent))
        disk_stats = psutil.disk_io_counters()
        self.log_queue.append(llog.new_line(llog.LogType.DISK_READ, (
            disk_stats.read_count, disk_stats.read_bytes / (1 << 10), disk_stats.read_time)))
        self.log_queue.append(llog.new_line(llog.LogType.DISK_WRITE, (
            disk_stats.write_count, disk_stats.write_bytes / (1 << 10), disk_stats.write_time)))

    def run(self):
        """
        Start an infinite loop with specified frequency and poll.
        """
        elapsed = 0
        process_set = set(psutil.process_iter())

        while True:
            start_time = time.perf_counter()

            # Re-calculuate time left for next polls.
            self.et_res_poll -= elapsed
            self.et_proc_poll -= elapsed

            if self.et_res_poll <= 0:
                # poll system resources.
                self._poll_sys_res()
                self.et_res_poll = self.res_poll_period

            if self.et_proc_poll <= 0:
                # poll processes here.
                newset = set(psutil.process_iter())
                setdiff = newset - process_set
                for p in setdiff:
                    try:
                        t = None
                        with p.oneshot():
                            t = (p.name(), p.cpu_times().user)
                        self.log_queue.append(llog.new_line(
                            llog.LogType.NEW_PROCESS, t))
                    except:
                        pass  # Suppress errors..
                process_set = newset

            elapsed = time.perf_counter() - start_time
            if elapsed < self.delta:
                time.sleep(self.delta - elapsed)
                elapsed = self.delta


class Sniffer:
    """
    Use scapy's AsyncSniffer to sniff packets
    """

    def __init__(self):
        """
        Constructor.
        """
        self.log_queue = []
        self.sniffer = AsyncSniffer(
            prn=self._append_packet, filter='tcp and ip', store=None)
        self.sniffer.start()

    def stop(self):
        """
        Stop. 
        """
        self.sniffer.stop()

    def _append_packet(self, x):
        # Check if it is HTTP or if the destination port is 443 (HTTPS)
        if x.haslayer(HTTPRequest) or x[TCP].dport == 443:
            self.log_queue.append(llog.new_line(
                llog.LogType.NET_CAPTURE, (x[IP].src, x[IP].dst)))
