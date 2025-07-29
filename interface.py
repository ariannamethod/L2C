import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import l2c


class ChatHandler(BaseHTTPRequestHandler):
    def _send_file(self, path, content_type):
        try:
            with open(path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self._send_file('index.html', 'text/html')
        elif self.path == '/style.css':
            self._send_file('style.css', 'text/css')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != '/chat':
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        try:
            payload = json.loads(data)
            prompt = payload.get('prompt', '')
        except Exception:
            self.send_response(400)
            self.end_headers()
            return
        try:
            text = l2c.generate(prompt, steps=32)
        except Exception as exc:  # pylint: disable=broad-except
            text = f'error: {exc}'
        resp = json.dumps({'response': text}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(resp)


def create_server():
    return HTTPServer(("", 8000), ChatHandler)


def main() -> None:
    server = create_server()
    print("Serving on http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
