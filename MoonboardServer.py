# Moonboard Server

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

class moonboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "moonboard.html"):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            document = "moonboard.html"
            f = open(document)
            self.wfile.write(f.read().encode())
        elif self.path == '/image/mini.png':
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            self.wfile.write(open('./image/mini.png', 'rb').read())
        elif self.path == '/image/climbingshoes.ico':
            self.send_response(200)
            self.send_header('Content-Type', 'image/x-icon')
            self.end_headers()
            self.wfile.write(open('./image/climbingshoes.ico', 'rb').read())
        elif self.path == '/get_problems':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with open('saved_climbs.json', 'r') as f:
                problems = json.load(f)
            self.wfile.write(json.dumps(problems).encode())
        else:
            self.send_response(404, "NOT FOUND")

    def do_POST(self):
        save_problem = True
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)
        if "name" in data:
            f = open('saved_climbs.json', 'r')
            saved_climbs = json.load(f)
            f.close()
            if len(saved_climbs['problems']) != 0:
                for name in saved_climbs['problems']:
                    # If name already exsists send error
                    if name['name'] == data['name']:
                        self.send_response(409, "Name already exists")
                        save_problem = False
                        break
            if (save_problem):
                saved_climbs['problems'].append(data)
                f = open('saved_climbs.json', 'w')
                json.dump(saved_climbs, f, ensure_ascii=False, indent=4)
                f.close()
        else:
            print("SIGNAL new problem: " + json.dumps(data))

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write("Recieved updated problem".encode())

def main():
    PORT = 8000
    server = HTTPServer(('', PORT), moonboardHandler)
    print('Servers started at PORT %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()