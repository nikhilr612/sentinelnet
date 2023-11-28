import redis
from redis.commands.json.path import Path
from server import Server
from llog import LogType

PREFIX_S = "computer"

# TODO Either choose a long-term database or use redis as the database
r = redis.Redis(host='localhost', port=6379, db=0)


def action(mac_addr, data):
    dev_id = PREFIX_S + ':' + mac_addr
    if not r.json().get(dev_id):
        # Create the details
        r.json().set(dev_id, Path.root_path(), {})
        r.json().set(dev_id, 'cpu_usage', [])
        r.json().set(dev_id, 'mem_usage', [])
        r.json().set(dev_id, 'disk_write', [])
        r.json().set(dev_id, 'disk_read', [])
        r.json().set(dev_id, 'processes', [])
        # TODO Add Network packet captures.

    # TODO Refactor to uniformly store to database using enum metadata
    for log in data:
        log_type = LogType(log[1])
        data_point = (
            log[0], *log[2]) if log_type.has_tuple() else (log[0], log[2])
        r.json().arrappend(dev_id, log_type.name.lower(), data_point)


if __name__ == "__main__":
    s = Server(target=action)
    s.start()
