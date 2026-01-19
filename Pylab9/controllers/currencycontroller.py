from controllers.databasecontroller import DatabaseController
from models.currency import Currency
from services.currencies_api import CurrencyAPIService
import logging
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    import io
    import base64
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

logger = logging.getLogger(__name__)


class CurrencyController:
    def __init__(self, db_controller: DatabaseController):
        self.db = db_controller
        self.api_service = CurrencyAPIService()

    def list_currencies(self):
        return self.db._read_currencies()

    def get_all_currencies(self):
        return self.list_currencies()

    def get_currency_by_id(self, currency_id: int) -> Currency:
        data = self.db._read_currency_by_id(currency_id)
        if data:
            return Currency.from_dict(data)
        return None

    def delete_currency(self, currency_id: int) -> bool:
        return self.db._delete_currency(currency_id)

    def create_currency(self, num_code: str, char_code: str, name: str,
                       value: float, nominal: int = 1) -> Currency:
        currency = Currency(num_code, char_code, name, value, nominal)

        currency_data = {
            'num_code': currency.num_code,
            'char_code': currency.char_code,
            'name': currency.name,
            'value': currency.value,
            'nominal': currency.nominal
        }

        currency_id = self.db._create_currency(currency_data)
        currency = Currency(num_code, char_code, name, value, nominal, currency_id)

        logger.info(f"Создана валюта: {char_code} (ID: {currency_id})")
        return currency

    def print_currencies(self):
        currencies = self.list_currencies()
        print("\n" + "=" * 80)
        print("СПИСОК ВАЛЮТ В БАЗЕ ДАННЫХ")
        print("=" * 80)
        print(f"{'ID':<5} {'Код':<6} {'Название':<30} {'Курс':<12} {'Номинал':<8}")
        print("-" * 80)
        for curr in currencies:
            print(f"{curr['id']:<5} {curr['char_code']:<6} {curr['name']:<30} "
                  f"{curr['value']:<12.4f} {curr['nominal']:<8}")
        print("=" * 80)
        print(f"Всего валют: {len(currencies)}")
        print("=" * 80 + "\n")

    def update_currencies_from_api(self) -> dict:
        return self.sync_with_api()

    def sync_with_api(self) -> dict:
        api_currencies = self.api_service.fetch_all_currencies()

        db_currencies = self.db._read_currencies()
        db_codes = {c['char_code'] for c in db_currencies}

        updated = 0
        errors = []

        for code in db_codes:
            try:
                if code in api_currencies:
                    value = api_currencies[code].get('Value', 0)
                    if self.db._update_currency(code, value):
                        updated += 1
                    else:
                        errors.append(f"Не удалось обновить валюту {code}")
                else:
                    errors.append(f"Валюта {code} не найдена в API")
            except Exception as e:
                errors.append(f"Ошибка при обновлении {code}: {str(e)}")

        return {
            'updated': updated,
            'errors': errors
        }

    def generate_user_charts(self, user_id: int) -> dict:
        if not MATPLOTLIB_AVAILABLE:
            return {'error': 'matplotlib не установлен'}

        user_currencies = self.db._read_user_currencies(user_id)
        charts = {}

        for currency in user_currencies:
            char_code = currency['char_code']
            currency_name = currency['name']

            try:
                historical_data = self.api_service.fetch_historical_currency_data(char_code, months=4)

                if historical_data:
                    dates = [datetime.strptime(d['Date'], '%Y-%m-%dT%H:%M:%S') for d in historical_data]
                    values = [d['Value'] for d in historical_data]

                    plt.figure(figsize=(10, 5))
                    plt.plot(dates, values, 'b-', linewidth=2, marker='o', markersize=3)
                    plt.title(f'Курс {char_code} ({currency_name}) за 4 месяца', fontsize=14, fontweight='bold')
                    plt.xlabel('Дата', fontsize=12)
                    plt.ylabel('Курс (рублей)', fontsize=12)
                    plt.grid(True, alpha=0.3)
                    plt.gcf().autofmt_xdate()

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                    buf.seek(0)
                    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                    plt.close('all')

                    charts[char_code] = {
                        'name': currency_name,
                        'chart': image_base64
                    }
                else:
                    charts[char_code] = {
                        'name': currency_name,
                        'error': 'Нет данных за последние 4 месяца'
                    }

            except Exception as e:
                charts[char_code] = {
                    'name': currency_name,
                    'error': f'Ошибка генерации графика: {str(e)}'
                }

        return charts