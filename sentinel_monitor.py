import redis
import numpy as np
import pandas as pd
import os
import sys
r = redis.Redis(host='localhost', port=6379, db=0)
dev = 'computer:ff:ff:ff:ff:ff:ff'

cpu = np.array(r.json().get(dev, 'cpu_usage'))
mem = np.array(r.json().get(dev, 'mem_usage'))
net = np.array(r.json().get(dev, 'net_capture'))
disk_read = np.array(r.json().get(dev, 'disk_read'))
disk_write = np.array(r.json().get(dev, 'disk_write'))

cpu_df = pd.DataFrame(cpu, columns=['timestamp', 'cpu_usage'])
mem_df = pd.DataFrame(mem, columns=['timestamp', 'memory_usage'])
net_df = pd.DataFrame(net, columns=['timestamp', 'src', 'dst'])
disk_read_df = pd.DataFrame(disk_read, columns=['timestamp', 'count', 'bytes', 'time'])
disk_write_df = pd.DataFrame(disk_write, columns=['timestamp', 'count', 'bytes', 'time'])

cpu_df['timestamp'] = pd.to_numeric(cpu_df['timestamp']).astype(int)
mem_df['timestamp'] = pd.to_numeric(mem_df['timestamp']).astype(int)
net_df['timestamp'] = pd.to_numeric(net_df['timestamp']).astype(int)
disk_read_df['timestamp'] = pd.to_numeric(disk_read_df['timestamp']).astype(int)
disk_write_df['timestamp'] = pd.to_numeric(disk_write_df['timestamp']).astype(int)

cpu_df = cpu_df.drop_duplicates(subset=['timestamp'])
mem_df = mem_df.drop_duplicates(subset=['timestamp'])
# Ignore net as it's not time sensitive
disk_read_df = disk_read_df.drop_duplicates(subset=['timestamp'])
disk_write_df = disk_write_df.drop_duplicates(subset=['timestamp'])

cpu_df.to_csv('cpu.csv', index=False)
mem_df.to_csv('mem.csv', index=False)
net_df.to_csv('net.csv', index=False)
disk_read_df.to_csv('disk_read.csv', index=False)
disk_write_df.to_csv('disk_write.csv', index=False)

os.system(f"{sys.executable} -m merlion.dashboard")