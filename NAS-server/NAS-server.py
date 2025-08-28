import time
import os
import socket
import threading
import bin.server_class as sc
import bin.shell as shell

NAME = socket.gethostname()
IP = socket.gethostbyname(NAME)

try:
    out = shell.run_command("ifconfig")
    t = out[out.index("wlan0"):]
    if "inet " in t:
        IP = t[t.index("inet ")+5: t.index("netmask")-1]
        IP = IP[:IP.index(" ")] if " " in IP else IP
    
    else:
        print(f'no internet connection switching to local ip:{IP}\n')

except Exception as e:
    print(f'failed to fetch ip\nError: {e}')
    IP = input('input machines ip: ')

PORT = int(input("Server on port (49152-65535)? "))
TIME = int(input("Server runtime in minute? "))
path = input("Complete path? ")

assert PORT in range(49152, 65535), "port selected is not a dynamic port use(49152-65535)"
assert os.path.exists(path), "invalid path"

startTime = time.time()//60

localServer = sc.server(port=PORT, path=path)
localServer.start()

link = f"http://{IP}:{PORT}"
print(f"server running at: {link}\n")

while True:
    
    if time.time()//60 - startTime >= TIME:
        print("\nclosing server, time elpse reached")
        os._exit(0)
