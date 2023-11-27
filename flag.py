import redis
from time import sleep

r = redis.Redis(host='localhost', port=6379, db=0)

whitelist = set()
with open('whitelist.txt') as file:
    for line in file.readlines():
        if line[0]!=';':
            whitelist.add(line.strip())

while True:
    while r.json().arrlen('computer:1','processes'):
        proc = r.json().arrpop('computer:1','processes')[1]
        if proc not in whitelist:
            print(f'Unauthorized Process: {proc}') # TODO Create alert on GUI
    sleep(10)