from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.main_controller import handle_request

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        result = handle_request(self.path, {})
        self.send_response(result["status"])
        self.send_header("Content-Type", result.get("content_type", "text/plain; charset=utf-8"))
        self.end_headers()
        self.wfile.write(result["content"].encode("utf-8"))

def run():
    server = HTTPServer(("localhost", 8000), AppHandler)
    print("Сервер запущен на http://localhost:8000")
    print("Нажмите Ctrl+C для остановки")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        server.server_close()

if __name__ == "__main__":
    run()