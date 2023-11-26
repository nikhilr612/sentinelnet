from enum import Enum
from collections import namedtuple
from datetime import datetime, timezone
from msgpack import ExtType

LOG_TYPE_CODE = 42


class LogType(Enum):
    """
    Enum for types of log lines.
    """
    CPU_USAGE = 0   # Log type for CPU usage.      data: float
    MEM_USAGE = 1   # Log type for Memory usage.   data: float
    NEW_PROCESS = 2  # Log type for new processes   data: (name, cpu_percent)
    NET_CAPTURE = 3  # Log type for incoming packets.
    DISK_READ = 4   # Log type for disk read       data: (count, bytes, time)
    DISK_WRITE = 5   # Log type for disk write      data: (count, bytes, time)


LogLine = namedtuple("LogLine", ['timestamp', 'logtype', 'data'])


def new_line(logtype, data):
    unix_epoch = datetime.now(timezone.utc).timestamp() * 1000
    return LogLine(unix_epoch, logtype, data)


def msgpack_hook(obj):
    if isinstance(obj, LogType):
        return ExtType(LOG_TYPE_CODE, obj.value.to_bytes(1))
    raise TypeError("Unknown type: %r" % (obj,))


def msgupack_hook(code, data):
    if code == LOG_TYPE_CODE:
        return int(data[0])
    return ExtType(code, data)
