from controllers.pages import PagesController
from controllers.currencycontroller import CurrencyController
from controllers.databasecontroller import DatabaseController


try:
    import matplotlib.pyplot as plt
    import io
    import base64
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def handle_request(path, query_params, db_controller, currency_controller, pages_controller):
    if path == '/':
        return handle_index(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/author':
        return handle_author(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/users':
        return handle_users(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/user':
        return handle_user(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/currencies':
        return handle_currencies(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/currency/delete':
        return handle_delete_currency(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/currency/show':
        return handle_show_currencies(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/currency/add':
        return handle_add_currency(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/currency/update_all':
        return handle_update_all_currencies(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/user/subscribe':
        return handle_subscribe(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/user/unsubscribe':
        return handle_unsubscribe(query_params, db_controller, currency_controller, pages_controller)
    elif path == '/user/charts':
        return handle_user_charts(query_params, db_controller, currency_controller, pages_controller)
    else:
        return handle_not_found(path, query_params, db_controller, currency_controller, pages_controller)


def handle_index(params, db_controller, currency_controller, pages_controller):
    html = pages_controller.render_index()
    return {
        "status": 200,
        "content": html,
        "content_type": "text/html; charset=utf-8"
    }


def handle_author(params, db_controller, currency_controller, pages_controller):
    html = pages_controller.render_author()
    return {
        "status": 200,
        "content": html,
        "content_type": "text/html; charset=utf-8"
    }


def handle_users(params, db_controller, currency_controller, pages_controller):
    html = pages_controller.render_users()
    return {
        "status": 200,
        "content": html,
        "content_type": "text/html; charset=utf-8"
    }


def handle_user(params, db_controller, currency_controller, pages_controller):
    try:
        id_list = params.get('id', ['1'])
        user_id = int(id_list[0] if isinstance(id_list, list) else id_list)
        message_list = params.get('message', [''])
        message = message_list[0] if isinstance(message_list, list) else message_list
    except (ValueError, IndexError, TypeError):
        user_id = 1
        message = ""

    html = pages_controller.render_user(user_id, message)
    return {
        "status": 200,
        "content": html,
        "content_type": "text/html; charset=utf-8"
    }


def handle_currencies(params, db_controller, currency_controller, pages_controller):
    message_list = params.get('message', [''])
    update_message = message_list[0] if isinstance(message_list, list) else message_list
    html = pages_controller.render_currencies(update_message)
    return {
        "status": 200,
        "content": html,
        "content_type": "text/html; charset=utf-8"
    }


def handle_delete_currency(params, db_controller, currency_controller, pages_controller):
    try:
        id_list = params.get('id', ['0'])
        currency_id = int(id_list[0] if isinstance(id_list, list) else id_list)
        if currency_id > 0:
            success = currency_controller.delete_currency(currency_id)
            if success:
                return {
                    "status": 302,
                    "content": "",
                    "headers": {"Location": "/currencies?message=Валюта+удалена"}
                }
            else:
                return {
                    "status": 404,
                    "content": "<h1>Валюта не найдена</h1>",
                    "content_type": "text/html; charset=utf-8"
                }
        else:
            return {
                "status": 400,
                "content": "<h1>Не указан ID валюты</h1>",
                "content_type": "text/html; charset=utf-8"
            }
    except (ValueError, TypeError, IndexError):
        return {
            "status": 400,
            "content": "<h1>Неверный ID валюты</h1>",
            "content_type": "text/html; charset=utf-8"
        }


def handle_show_currencies(params, db_controller, currency_controller, pages_controller):
    currency_controller.print_currencies()
    return {
        "status": 200,
        "content": "<h1>Курсы валют выведены в консоль сервера</h1>",
        "content_type": "text/html; charset=utf-8"
    }


def handle_add_currency(params, db_controller, currency_controller, pages_controller):
    code_list = params.get('code', [])
    if not code_list:
        html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Добавить валюту</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            form { max-width: 300px; }
            input { padding: 8px; width: 100%; margin: 10px 0; }
            button { padding: 8px 15px; background: #0066cc; color: white; border: none; cursor: pointer; }
            button:hover { background: #0052a3; }
        </style>
    </head>
    <body>
        <h1>Добавить валюту</h1>
        <form method="get" action="/currency/add">
            <input type="text" name="code" placeholder="Код валюты (3 буквы, например USD)" maxlength="3" required>
            <button type="submit">Добавить</button>
        </form>
        <br>
        <a href="/currencies">Вернуться к списку валют</a>
    </body>
    </html>
    """
        return {
            "status": 200,
            "content": html,
            "content_type": "text/html; charset=utf-8"
        }

    char_code = code_list[0].upper()

    if len(char_code) != 3:
        return {
            "status": 302,
            "content": "",
            "headers": {"Location": "/currencies?message=Код+валюты+должен+быть+из+3+букв"}
        }

    from services.currencies_api import CurrencyAPIService
    api_service = CurrencyAPIService()
    all_currencies = api_service.fetch_all_currencies()

    if char_code not in all_currencies:
        return {
            "status": 302,
            "content": "",
            "headers": {"Location": "/currencies?message=Валюта+не+найдена+в+API"}
        }

    currency_data = all_currencies[char_code]
    num_code = str(currency_data.get('NumCode', '000'))
    name = currency_data.get('Name', '')
    value = currency_data.get('Value', 0)
    nominal = currency_data.get('Nominal', 1)

    try:
        currency_controller.create_currency(num_code, char_code, name, value, nominal)
        return {
            "status": 302,
            "content": "",
            "headers": {"Location": f"/currencies?message=Валюта+{char_code}+добавлена"}
        }
    except ValueError as e:
        if "уже существует" in str(e):
            return {
                "status": 302,
                "content": "",
                "headers": {"Location": f"/currencies?message=Валюта+{char_code}+уже+существует"}
            }
        else:
            return {
                "status": 302,
                "content": "",
                "headers": {"Location": f"/currencies?message=Ошибка+валидации:+{str(e).replace(' ', '+')}"}
            }
    except Exception as e:
        return {
            "status": 302,
            "content": "",
            "headers": {"Location": f"/currencies?message=Ошибка:+{str(e).replace(' ', '+')}"}
        }


def handle_update_all_currencies(params, db_controller, currency_controller, pages_controller):
    try:
        result = currency_controller.update_currencies_from_api()
        message = f"Обновлено {result['updated']} валют"
        if result['errors']:
            message += f". Ошибки: {', '.join(result['errors'][:3])}"
        encoded_message = "&message=" + "+".join(message.split())
        return {
            "status": 302,
            "content": "",
            "headers": {"Location": f"/currencies{encoded_message}"}
        }
    except Exception as e:
        return {
            "status": 302,
            "content": "",
            "headers": {"Location": "/currencies?message=Ошибка+при+обновлении"}
        }


def handle_subscribe(params, db_controller, currency_controller, pages_controller):
    try:
        user_id_list = params.get('user_id', ['0'])
        currency_id_list = params.get('currency_id', ['0'])
        user_id = int(user_id_list[0] if isinstance(user_id_list, list) else user_id_list)
        currency_id = int(currency_id_list[0] if isinstance(currency_id_list, list) else currency_id_list)

        if user_id > 0 and currency_id > 0:
            success = db_controller._subscribe_user_to_currency(user_id, currency_id)
            if success:
                return {
                    "status": 302,
                    "content": "",
                    "headers": {"Location": f"/user?id={user_id}&message=Подписка+оформлена"}
                }
            else:
                return {
                    "status": 302,
                    "content": "",
                    "headers": {"Location": f"/user?id={user_id}&message=Уже+подписан"}
                }
        else:
            return {
                "status": 400,
                "content": "<h1>Неверные параметры</h1>",
                "content_type": "text/html; charset=utf-8"
            }
    except (ValueError, TypeError, IndexError):
        return {
            "status": 400,
            "content": "<h1>Неверные параметры</h1>",
            "content_type": "text/html; charset=utf-8"
        }


def handle_unsubscribe(params, db_controller, currency_controller, pages_controller):
    try:
        user_id_list = params.get('user_id', ['0'])
        currency_id_list = params.get('currency_id', ['0'])
        user_id = int(user_id_list[0] if isinstance(user_id_list, list) else user_id_list)
        currency_id = int(currency_id_list[0] if isinstance(currency_id_list, list) else currency_id_list)

        if user_id > 0 and currency_id > 0:
            success = db_controller._unsubscribe_user_from_currency(user_id, currency_id)
            if success:
                return {
                    "status": 302,
                    "content": "",
                    "headers": {"Location": f"/user?id={user_id}&message=Отписка+выполнена"}
                }
            else:
                return {
                    "status": 302,
                    "content": "",
                    "headers": {"Location": f"/user?id={user_id}&message=Не+был+подписан"}
                }
        else:
            return {
                "status": 400,
                "content": "<h1>Неверные параметры</h1>",
                "content_type": "text/html; charset=utf-8"
            }
    except (ValueError, TypeError, IndexError):
        return {
            "status": 400,
            "content": "<h1>Неверные параметры</h1>",
            "content_type": "text/html; charset=utf-8"
        }


def handle_user_charts(params, db_controller, currency_controller, pages_controller):
    user_id_list = params.get('user_id', [])
    if not user_id_list:
        return {
            "status": 400,
            "content": "<h1>Не указан ID пользователя</h1>",
            "content_type": "text/html; charset=utf-8"
        }

    user_id = int(user_id_list[0])

    try:
        user = db_controller._read_user_by_id(user_id)
        if not user:
            return {
                "status": 404,
                "content": "<h1>Пользователь не найден</h1>",
                "content_type": "text/html; charset=utf-8"
            }

        charts = currency_controller.generate_user_charts(user_id)
        html = pages_controller.render_user_charts(user, charts)
        return {
            "status": 200,
            "content": html,
            "content_type": "text/html; charset=utf-8"
        }

    except Exception as e:
        return {
            "status": 500,
            "content": f"<h1>Ошибка при генерации графиков: {str(e)}</h1>",
            "content_type": "text/html; charset=utf-8"
        }


def handle_not_found(path, params, db_controller, currency_controller, pages_controller):
    return {
        "status": 404,
        "content": f"<h1>404 - Страница {path} не найдена</h1>",
        "content_type": "text/html; charset=utf-8"
    }