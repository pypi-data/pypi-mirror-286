import time
import server
import ws
ws.run()
server.run()

while server.web_server_thread.is_alive() and not server.stop:
    time.sleep(0.5)
