from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from jinja2 import Environment, FileSystemLoader
    JINJA_AVAILABLE = True
except ImportError:
    JINJA_AVAILABLE = False

from controllers.main_controller import handle_request
from controllers.databasecontroller import DatabaseController
from controllers.currencycontroller import CurrencyController
from controllers.pages import PagesController


class AppHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, db_controller=None, currency_controller=None, pages_controller=None, **kwargs):
        self.db_controller = db_controller
        self.currency_controller = currency_controller
        self.pages_controller = pages_controller
        super().__init__(*args, **kwargs)

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        result = handle_request(path, query_params, self.db_controller, self.currency_controller, self.pages_controller)

        self.send_response(result["status"])

        if "headers" in result:
            for header, value in result["headers"].items():
                self.send_header(header, value)

        self.send_header("Content-Type", result.get("content_type", "text/plain; charset=utf-8"))
        self.end_headers()
        self.wfile.write(result["content"].encode("utf-8"))


def run():
    if not JINJA_AVAILABLE:
        print("Ошибка: jinja2 не установлен. Установите зависимости: pip install -r requirements.txt")
        return

    from jinja2 import Environment, FileSystemLoader
    import datetime
    jinja_env = Environment(loader=FileSystemLoader('templates'))
    jinja_env.filters['now'] = lambda format: datetime.datetime.now().strftime(format)

    db_controller = DatabaseController()
    currency_controller = CurrencyController(db_controller)
    pages_controller = PagesController(jinja_env, db_controller, currency_controller)

    def handler_class(*args, **kwargs):
        return AppHandler(*args, db_controller=db_controller, currency_controller=currency_controller, pages_controller=pages_controller, **kwargs)

    server = HTTPServer(("localhost", 8000), handler_class)
    print("Сервер запущен на http://localhost:8000")
    print("Нажмите Ctrl+C для остановки")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        server.server_close()


if __name__ == "__main__":
    run()