from enum import Enum
from collections import namedtuple
from datetime import datetime, timezone
from msgpack import ExtType
from sys import byteorder

LOG_TYPE_CODE = 42


class LogType(Enum):
    """Enum for types of log lines."""
    CPU_USAGE = 1     # Log type for CPU usage.         data: float
    MEM_USAGE = 2     # Log type for Memory usage.      data: float
    # Log type for new processes      data: str   (process name)
    NEW_PROCESS = 3
    NET_CAPTURE = -4  # Log type for incoming packets.
    # Log type for disk read          data: (count, bytes, time)
    DISK_READ = -5
    # Log type for disk write         data: (count, bytes, time)
    DISK_WRITE = -6

    def has_tuple(self):
        """
        Returns True if this LogType is accompanied by tuple data.
        """
        return self.value < 0


LogLine = namedtuple("LogLine", ['timestamp', 'logtype', 'data'])


def new_line(logtype, data):
    unix_epoch = datetime.now(timezone.utc).timestamp() * 1000
    return LogLine(unix_epoch, logtype, data)


def msgpack_hook(obj):
    if isinstance(obj, LogType):
        return ExtType(LOG_TYPE_CODE, obj.value.to_bytes(1, byteorder, signed=True))
    raise TypeError("Unknown type: %r" % (obj,))


def msgupack_hook(code, data):
    if code == LOG_TYPE_CODE:
        return int.from_bytes(data, byteorder, signed=True)
    return ExtType(code, data)
