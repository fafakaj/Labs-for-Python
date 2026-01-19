from jinja2 import Environment, TemplateNotFound
from controllers.databasecontroller import DatabaseController
from controllers.currencycontroller import CurrencyController


class PagesController:
    def __init__(self, jinja_env: Environment, db_controller: DatabaseController, currency_controller: CurrencyController):
        self.env = jinja_env
        self.db = db_controller
        self.currency_controller = currency_controller

    def render_template(self, template_name: str, **context) -> str:
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except TemplateNotFound:
            return f"<h1>Шаблон {template_name} не найден</h1>"
        except Exception as e:
            return f"<h1>Ошибка рендеринга шаблона: {str(e)}</h1>"

    def render_index(self) -> str:
        return self.render_template(
            'index.html',
            title='Currency Tracker v2.0'
        )

    def render_author(self) -> str:
        return self.render_template(
            'author.html',
            title='Об авторе',
            author_name='Лесницкий Александр Маркович',
            student_info='Студент 1 курса, группа P3123',
            direction='Нейротехнологии и программирование',
            faculty='ПИиКТ',
            university='ИТМО',
            email='mrainxxxm@gmail.com'
        )

    def render_users(self) -> str:
        users = self.db._read_users()

        users_with_subscriptions = []
        for user in users:
            user_currencies = self.db._read_user_currencies(user['id'])
            user['currency_count'] = len(user_currencies)
            users_with_subscriptions.append(user)

        return self.render_template(
            'users.html',
            title='Пользователи системы',
            users=users_with_subscriptions
        )

    def render_user(self, user_id: int, message: str = "") -> str:
        user = self.db._read_user_by_id(user_id)
        if not user:
            return self.render_template(
                'error.html',
                title='Ошибка',
                message='Пользователь не найден'
            )

        user_currencies = self.db._read_user_currencies(user_id)
        all_currencies = self.db._read_all_currencies_for_user(user_id)

        return self.render_template(
            'user.html',
            title=f'Пользователь: {user["name"]}',
            user=user,
            currencies=user_currencies,
            all_currencies=all_currencies,
            message=message
        )

    def render_currencies(self, update_message: str = "") -> str:
        currencies = self.currency_controller.get_all_currencies()

        return self.render_template(
            'currencies.html',
            title='Валюты',
            currencies=currencies,
            update_message=update_message
        )

    def render_user_charts(self, user: dict, charts: dict) -> str:
        return self.render_template(
            'user_charts.html',
            user=user,
            charts=charts
        )