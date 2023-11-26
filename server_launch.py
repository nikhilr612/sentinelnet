import msgpack
import numpy as np
import redis
from server import Server
from llog import msgupack_hook, LogType

r = redis.Redis(host='localhost', port=6379, db=0)
if not r.exists('cpu_usage'):
    r.rpush('cpu_usage')
if not r.exists('mem_usage'):
    r.rpush('mem_usage')

def servlet_plot(conn):
    reader = conn.makefile(mode='rb')
    data = msgpack.unpack(reader, ext_hook=msgupack_hook)

    for log in data:
        if LogType(log[1]) == LogType.CPU_USAGE:
            r.rpush('cpu_usage',np.array((log[0], log[2])))
        if LogType(log[1]) == LogType.MEM_USAGE:
            mem_usage.append(np.array((log[0], log[2])))

    reader.close()
    conn.close()
    # TODO Connect to Redis or make respones transferrable to analysis and gui

s = Server(target=servlet_plot)
s.start()
