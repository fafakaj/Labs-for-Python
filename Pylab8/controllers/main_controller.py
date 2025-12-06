import urllib.parse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from models import Author, App, User

from utils.currencies_api import get_currencies, get_all_currencies

main_author = Author(name="Лесницикй Александр", group="P3123")
app_info = App(name="Currency Tracker", version="1.0", author=main_author)

users_db = {
    1: User(1, "Иван Резников"),
    2: User(2, "Игорек"),
    3: User(3, "Максим общежитие"),
}

TOP_CURRENCIES = [
    "USD",
    "EUR",
    "CNY",
    "GBP",
    "CHF",
    "JPY",
    "TRY",
    "INR",
    "KRW",
    "SGD",
    "AUD",
    "CAD",
    "NOK",
    "SEK",
    "DKK",
]

# Подписки: user_id → set(char_code)
user_subscriptions = {
    1: {"USD", "EUR"},
    2: {"CNY", "GBP"},
    3: {"USD", "JPY", "EUR"},
}

currency_history = {
    "USD": [
        {"date": "2025-09", "value": 92.1},
        {"date": "2025-10", "value": 92.8},
        {"date": "2025-11", "value": 93.5},
        {"date": "2025-12", "value": 94.2},
    ],
    "EUR": [
        {"date": "2025-09", "value": 100.5},
        {"date": "2025-10", "value": 101.2},
        {"date": "2025-11", "value": 102.0},
        {"date": "2025-12", "value": 102.7},
    ],
    "CNY": [
        {"date": "2025-09", "value": 12.8},
        {"date": "2025-10", "value": 12.9},
        {"date": "2025-11", "value": 13.0},
        {"date": "2025-12", "value": 13.1},
    ],
    "GBP": [
        {"date": "2025-09", "value": 115.0},
        {"date": "2025-10", "value": 116.2},
        {"date": "2025-11", "value": 117.0},
        {"date": "2025-12", "value": 118.3},
    ],
    "JPY": [
        {"date": "2025-09", "value": 0.61},
        {"date": "2025-10", "value": 0.62},
        {"date": "2025-11", "value": 0.63},
        {"date": "2025-12", "value": 0.64},
    ],
}

template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape())


def render_template(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context)


def handle_request(path, query_params):
    parsed = urllib.parse.urlparse(path)
    route = parsed.path
    query = urllib.parse.parse_qs(parsed.query) if not query_params else query_params

    if route == "/":
        return handle_index()
    elif route == "/author":
        return handle_author()
    elif route == "/users":
        return handle_users()
    elif route == "/user":
        user_id = query.get("id", [None])[0]
        if user_id and user_id.isdigit():
            return handle_user(int(user_id))
        else:
            return {"status": 400, "content": "Требуется параметр id"}
    elif route == "/currencies":
        return handle_currencies()
    elif route == "/subscribe":
        return handle_subscribe(query)
    else:
        return {"status": 404, "content": "Страница не найдена"}


def handle_index():
    html = render_template("index.html", app=app_info)
    return {"status": 200, "content": html, "content_type": "text/html; charset=utf-8"}


def handle_author():
    html = render_template("author.html", author=main_author)
    return {"status": 200, "content": html, "content_type": "text/html; charset=utf-8"}


def handle_users():
    html = render_template("users.html", users=users_db.values())
    return {"status": 200, "content": html, "content_type": "text/html; charset=utf-8"}


def handle_user(user_id):
    user = users_db.get(user_id)
    if not user:
        return {"status": 404, "content": "Пользователь не найден"}

    subscribed = user_subscriptions.get(user_id, set())
    currencies = {}
    error = None

    if subscribed:
        try:
            currencies = get_currencies(list(subscribed))
        except Exception as e:
            error = str(e)

    chart_data = {}
    for code in subscribed:
        if code in currency_history:
            values = [point["value"] for point in currency_history[code]]
            dates = [point["date"] for point in currency_history[code]]
            chart_data[code] = {"dates": list(dates), "values": list(values)}

    html = render_template(
        "user.html",
        user=user,
        currencies=currencies,
        error=error,
        subscribed_codes=subscribed,
        chart_data=chart_data,
    )
    return {"status": 200, "content": html, "content_type": "text/html; charset=utf-8"}


def handle_currencies():
    try:
        raw = get_currencies(TOP_CURRENCIES)
        currencies = []
        for code in TOP_CURRENCIES:
            if code in raw:
                currencies.append({"char_code": code, "value": raw[code]})
        error = None
    except Exception as e:
        currencies = []
        error = str(e)

    html = render_template(
        "currencies.html", currencies=currencies, error=error, users_db=users_db
    )
    return {"status": 200, "content": html, "content_type": "text/html; charset=utf-8"}


def handle_subscribe(query):
    user_id = query.get("user_id", [None])[0]
    currency = query.get("currency", [None])[0]

    if not user_id or not user_id.isdigit():
        return {"status": 400, "content": "Ошибка: укажите корректный user_id"}
    if not currency or not isinstance(currency, str) or len(currency) != 3:
        return {
            "status": 400,
            "content": "Ошибка: укажите валюту в формате XXX (например, USD)",
        }

    user_id = int(user_id)
    currency = currency.upper()

    if user_id not in users_db:
        return {"status": 404, "content": "Пользователь не найден"}

    all_currencies = get_all_currencies()
    if currency not in all_currencies:
        return {
            "status": 400,
            "content": f"Ошибка: валюта '{currency}' не найдена в ЦБ РФ",
        }

    if user_id not in user_subscriptions:
        user_subscriptions[user_id] = set()
    user_subscriptions[user_id].add(currency)

    redirect_url = f"/user?id={user_id}"
    return {"status": 302, "content": "", "headers": {"Location": redirect_url}}
