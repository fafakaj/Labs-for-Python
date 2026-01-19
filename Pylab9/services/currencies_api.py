import requests
import sys
import functools
import logging
from datetime import datetime, timedelta


def logger(func=None, *, handle=sys.stdout):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            is_logger = hasattr(handle, "info") and callable(getattr(handle, "info"))
            if is_logger:
                handle.info(
                    f"[INFO] Вызов {f.__name__} c args = {args}, kwargs = {kwargs}"
                )
                try:
                    result = f(*args, **kwargs)
                    handle.info(f"[INFO] {f.__name__} вернула {result}")
                    return result
                except Exception as e:
                    handle.error(
                        f"[ERROR] {f.__name__} выбросила {type(e).__name__}: {e}"
                    )
                    raise
            else:
                handle.write(
                    f"[INFO] Вызов {f.__name__} c args = {args}, kwargs = {kwargs}\n"
                )
                try:
                    result = f(*args, **kwargs)
                    handle.write(f"[INFO] {f.__name__} вернула {result}\n")
                    return result
                except Exception as e:
                    handle.write(
                        f"[ERROR] {f.__name__} выбросила {type(e).__name__}: {e}\n"
                    )
                    raise

        return inner

    if func is None:
        return decorator
    else:
        return decorator(func)


def get_all_currencies(url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Valute" not in data:
            return {}
        return data["Valute"]
    except Exception:
        return {}


class CurrencyAPIService:
    def __init__(self, api_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"):
        self.api_url = api_url

    def fetch_all_currencies(self) -> dict:
        return get_all_currencies(self.api_url)

    def fetch_historical_currency_data(self, char_code: str, months: int = 4) -> list:
        import xml.etree.ElementTree as ET

        current_data = self.fetch_all_currencies()
        if not current_data or char_code not in current_data:
            return []

        currency_id = current_data[char_code].get('ID', '')
        if not currency_id:
            return []

        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        start_date_str = start_date.strftime('%d/%m/%Y')
        end_date_str = end_date.strftime('%d/%m/%Y')

        url = f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date_str}&date_req2={end_date_str}&VAL_NM_RQ={currency_id}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            historical_data = []

            for record in root.findall('Record'):
                date_str = record.get('Date')
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                        value_elem = record.find('Value')
                        if value_elem is not None and value_elem.text:
                            value_str = value_elem.text.replace(',', '.')
                            value = float(value_str)

                            historical_data.append({
                                'Date': date_obj.strftime('%Y-%m-%dT%H:%M:%S'),
                                'Value': value
                            })
                    except (ValueError, AttributeError) as e:
                        logging.warning(f"Ошибка при обработке записи для даты {date_str}: {e}")
                        continue

            historical_data.sort(key=lambda x: x['Date'])
            return historical_data

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при запросе к API ЦБ РФ: {e}")
            return []
        except ET.ParseError as e:
            logging.error(f"Ошибка при парсинге XML: {e}")
            return []
        except Exception as e:
            logging.error(f"Неожиданная ошибка при получении исторических данных: {e}")
            return []