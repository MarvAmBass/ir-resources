from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#from http.server import BaseHTTPRequestHandler, HTTPServer

import os
import json

remotes = dict()

def exec_cmd(command):
    return str(os.popen(command).read()[:-1])

def update_remotes():
    global remotes
    remotes = dict()

    data = exec_cmd("cat /etc/lirc/lircd.conf | grep 'name\|KEY_' | sed 's/name//g' | awk '{print $1}'")

    current_remote = None
    for line in data.split('\n'):
        if not line.startswith('KEY_'):
            current_remote = line
            remotes[current_remote] = list()
        else:
            if current_remote is not None:
                remotes[current_remote].append(line)

class HttpRestApiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/remotes'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                self.wfile.write((str(json.dumps(remotes, sort_keys=True, indent=4, separators=(',', ': ')))).encode("utf-8"))
                self.wfile.write(('\n').encode("utf-8"))

                return

        if self.path.startswith('/update'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                update_remotes()
                self.wfile.write((str(json.dumps({"status":"updated remotes"}, sort_keys=True, indent=4, separators=(',', ': ')))).encode("utf-8"))
                self.wfile.write(('\n').encode("utf-8"))

                return

        if self.path.startswith('/send/'):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                lirc_cmd = 'irsend -d /dev/lircd SEND_ONCE '

                # /send/ <remote> / <KEY>
                send_data = self.path.replace('/send/','').split('/')

                if send_data[1] in remotes[send_data[0]]:
                    exec_cmd(str(lirc_cmd + send_data[0] + ' ' + send_data[1]))

                    self.wfile.write((str(json.dumps({"status":"send"}, sort_keys=True, indent=4, separators=(',', ': ')))).encode("utf-8"))
                    self.wfile.write(('\n').encode("utf-8"))
                else:
                    self.wfile.write((str(json.dumps({"status":"error", "message": "remote and/or key not found"}, sort_keys=True, indent=4, separators=(',', ': ')))).encode("utf-8"))
                    self.wfile.write(('\n').encode("utf-8"))

                return

        self.send_response(500)
        self.end_headers()
        return

def main():
    update_remotes()
    try:
        server = HTTPServer(('', 8711), HttpRestApiHandler)
        print('started httpserver...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()
