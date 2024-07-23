import sys
import time
from ascript.ios.developer import server
from ascript.ios.developer import ws

ws.run()
server.run()

print("启动参数", sys.argv)

while server.web_server_thread.is_alive() and not server.stop:
    time.sleep(0.5)
