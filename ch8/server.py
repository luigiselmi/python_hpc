# This script implements an http server. A client can send a request using the argument
# name and delay. The connection is synchronous and will last for the delay time send in
# the request. the server can be started with the command
#
# $ python server.py
#
# The server will listen on port 8080 of localhost (127.0.0.1). The server can be shut down
# by killing its process using its process id. We first look for the id of the process listening
# on port 8080
#
# $ netstat -ano | findstr :8080
#
# The response will be something similar to 
#
# TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       2068
# TCP    [::]:8080              [::]:0                 LISTENING       2068
#
# Here the pid is 2068 so we kill the process with this id
#
# $ taskkill /PID 2068 /F
#

import json
import time
from collections import defaultdict
from tornado import gen, httpserver, ioloop, options, web
import os
import threading

options.define("port", default=8080, help="Port to serve on")


class AddMetric(web.RequestHandler):
    metric_data = defaultdict(list)

    async def get(self):
        if self.get_argument("flush", False):
            json.dump(self.metric_data, open("metric_data.json", "w+"))
        else:
            name = self.get_argument("name")
            try:
                delay = int(self.get_argument("delay", 1024))
            except ValueError:
                raise web.HTTPError(400, reason="Invalid value for delay")

            start = time.time()
            await gen.sleep(delay / 1000.0)
            self.write(".")
            self.finish()
            end = time.time()
            self.metric_data[name].append(
                {"start": start, "end": end, "dt": end - start}
            )
def threads_info():
    total_threads = threading.active_count()
    thread_name = threading.current_thread().name
    print(f'Python process running with process id: {os.getpid()}')
    print(f'Python is currently running {total_threads} thread(s)')
    print(f'The current thread is {thread_name}')

if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port

    application = web.Application([(r"/add", AddMetric)])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    threads_info()
    print(("Listening on port: {}".format(port)))
    ioloop.IOLoop.instance().start()