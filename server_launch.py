import redis
from redis.commands.json.path import Path
from server import Server
from llog import LogType
from pathlib import Path as stdPath
import argparse
import sys

PREFIX_S = "computer"

# TODO Either choose a long-term database or use redis as the database
r = redis.Redis(host='localhost', port=6379, db=0)
app = None

whitelist = set(stdPath('./whitelist.txt').read_text().split('\n'))

def action(mac_addr, data):
    dev_id = PREFIX_S + ':' + mac_addr
    if not r.json().get(dev_id):
        # Create the details
        r.json().set(dev_id, Path.root_path(), {})
        r.json().set(dev_id, 'cpu_usage', [])
        r.json().set(dev_id, 'mem_usage', [])
        r.json().set(dev_id, 'disk_write', [])
        r.json().set(dev_id, 'disk_read', [])
        r.json().set(dev_id, 'new_process', [])
        r.json().set(dev_id, 'net_capture', [])

    for log in data:
        log_type = LogType(log[1])
        if log_type == LogType.NEW_PROCESS:
            if not log[2] in whitelist:
                print(mac_addr, "has spawned non-whitelisted process")
                r.json().arrappend(dev_id, 'new_process', data_point)
            else:
                continue  # Don't bother with 'OK' processes.
        data_point = (
            log[0], *log[2]) if log_type.has_tuple() else (log[0], log[2])
        r.json().arrappend(dev_id, log_type.name.lower(), data_point)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='SentinelNet Server',
                    description='Headless server instance')
    parser.add_argument('-p', '--port', type=int, default=6444);
    parser.add_argument('-q','--qsize', type=int, default=5, help="Maximum number of connections that can be queued.");
    args = parser.parse_args();
    s = Server(port=args.port, queue=args.qsize, target=action)
    s.start()
