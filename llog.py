from enum import Enum
from collections import namedtuple
from datetime import datetime, timezone
from msgpack import ExtType

LOG_TYPE_CODE = 42

class LogType(Enum):
    """Enum for types of log lines."""
    CPU_USAGE = 1     # Log type for CPU usage.         data: float
    MEM_USAGE = 2     # Log type for Memory usage.      data: float
    NEW_PROCESS = 3   # Log type for new processes      data: str   (process name)
    NET_CAPTURE = -4  # Log type for incoming packets.
    DISK_READ = -5    # Log type for disk read          data: (count, bytes, time)
    DISK_WRITE = -6   # Log type for disk write         data: (count, bytes, time)

    def has_tuple(self):
        """
        Returns True if this LogType is accompanied by tuple data.
        """
        return self.value < 0;

    def __str__(self):
        """
        Return a 'user-friendly' name for the log type.
        """
        return {
            LogType.CPU_USAGE: 'cpu_usage',
            LogType.MEM_USAGE: 'mem_usage',
            LogType.NEW_PROCESS: 'processes',
            LogType.DISK_READ: 'disk_read',
            LogType.DISK_WRITE: 'disk_write',
            LogType.NET_CAPTURE: 'captures'
        }[self];

LogLine = namedtuple("LogLine", ['timestamp', 'logtype', 'data'])


def new_line(logtype, data):
    unix_epoch = datetime.now(timezone.utc).timestamp() * 1000
    return LogLine(unix_epoch, logtype, data)


def msgpack_hook(obj):
    if isinstance(obj, LogType):
        return ExtType(LOG_TYPE_CODE, obj.value.to_bytes(1, signed=True))
    raise TypeError("Unknown type: %r" % (obj,))


def msgupack_hook(code, data):
    if code == LOG_TYPE_CODE:
        return int.from_bytes(data, signed=True);
    return ExtType(code, data)
