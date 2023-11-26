import msgpack
import numpy as np
import redis
from redis.commands.json.path import Path
from server import Server
from llog import msgupack_hook, LogType

r = redis.Redis(host='localhost', port=6379, db=0)


def servlet_plot(conn):
    # TODO Add a way to distinguish between devices when storing to DB
    reader = conn.makefile(mode='rb')
    data = msgpack.unpack(reader, ext_hook=msgupack_hook)

    if not r.json().get('computer:1'):
        r.json().set('computer:1', Path.root_path(), {})

    for log in data:
        if LogType(log[1]) == LogType.CPU_USAGE:
            data_point = (log[0], log[2])

            if 'cpu_usage' in r.json().objkeys('computer:1'):
                r.json().arrappend('computer:1', 'cpu_usage', data_point)
            else:
                r.json().set('computer:1', 'cpu_usage', [data_point])

        if LogType(log[1]) == LogType.MEM_USAGE:
            data_point = (log[0], log[2])

            if 'mem_usage' in r.json().objkeys('computer:1'):
                r.json().arrappend('computer:1', 'mem_usage', data_point)
            else:
                r.json().set('computer:1', 'mem_usage', [data_point])

    reader.close()
    conn.close()


s = Server(target=servlet_plot)
s.start()
