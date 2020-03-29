import os
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.environ.get('PORT', 80))

class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/data.json'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "API by Hung Phu: http://ncov-api-hp.herokuapp.com or http://ncov-api-hp.herokuapp.com/data.json"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

httpd = HTTPServer(('', port), Serv)
httpd.serve_forever()