import sqlite3
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseController:
    def __init__(self, db_path: str = ':memory:'):
        """Инициализация подключения к БД SQLite в памяти"""
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
        self._insert_sample_data()
        logger.info("База данных инициализирована в памяти")

    def _create_tables(self):
        """Создание таблиц с первичными и внешними ключами"""
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            ''')

            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    num_code TEXT NOT NULL,
                    char_code TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    value REAL,
                    nominal INTEGER
                )
            ''')

            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS user_currency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    currency_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
                    FOREIGN KEY(currency_id) REFERENCES currency(id) ON DELETE CASCADE,
                    UNIQUE(user_id, currency_id)
                )
            ''')

            self.connection.execute('PRAGMA foreign_keys = ON')

        logger.info("Таблицы созданы: user, currency, user_currency")

    def _insert_sample_data(self):
        """Вставка тестовых данных с использованием параметризованных запросов"""
        cursor = self.connection.execute("SELECT COUNT(*) as count FROM currency")
        count = cursor.fetchone()['count']

        if count == 0:
            try:
                currencies = [
                    {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.5, "nominal": 1},
                    {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 98.7, "nominal": 1},
                    {"num_code": "643", "char_code": "RUB", "name": "Российский рубль", "value": 1.0, "nominal": 1},
                    {"num_code": "392", "char_code": "JPY", "name": "Японская иена", "value": 0.61, "nominal": 100},
                    {"num_code": "826", "char_code": "GBP", "name": "Фунт стерлингов", "value": 115.2, "nominal": 1},
                    {"num_code": "756", "char_code": "CHF", "name": "Швейцарский франк", "value": 103.5, "nominal": 1},
                    {"num_code": "156", "char_code": "CNY", "name": "Китайский юань", "value": 12.8, "nominal": 1}
                ]

                sql = """
                    INSERT INTO currency(num_code, char_code, name, value, nominal)
                    VALUES(:num_code, :char_code, :name, :value, :nominal)
                """
                self.connection.executemany(sql, currencies)

                users = [
                    {"name": "Иван Резников"},
                    {"name": "Максим общежитие"},
                    {"name": "Игорек"}
                ]

                sql_user = "INSERT INTO user(name) VALUES(:name)"
                self.connection.executemany(sql_user, users)

                subscriptions = [
                    {"user_id": 1, "currency_id": 1},  # Иван Резников - USD
                    {"user_id": 1, "currency_id": 2},  # Иван Резников - EUR
                    {"user_id": 2, "currency_id": 1},  # Максим общежитие - USD
                    {"user_id": 2, "currency_id": 3},  # Максим общежитие - RUB
                    {"user_id": 3, "currency_id": 4},  # Игорек - JPY
                    {"user_id": 3, "currency_id": 5},  # Игорек - GBP
                ]

                sql_sub = "INSERT INTO user_currency(user_id, currency_id) VALUES(:user_id, :currency_id)"
                self.connection.executemany(sql_sub, subscriptions)

                self.connection.commit()
                logger.info(
                    f"Добавлено {len(currencies)} валют, {len(users)} пользователей и {len(subscriptions)} подписок")

            except sqlite3.Error as e:
                logger.error(f"Ошибка при вставке тестовых данных: {e}")
                self.connection.rollback()

    def _create_currency(self, currency_data: Dict[str, Any]) -> int:
        """Create: добавление новой валюты"""
        try:
            sql = """
                INSERT INTO currency(num_code, char_code, name, value, nominal)
                VALUES(:num_code, :char_code, :name, :value, :nominal)
            """
            cursor = self.connection.execute(sql, currency_data)
            self.connection.commit()
            logger.info(f"Создана валюта: {currency_data['char_code']}")
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            logger.error(f"Ошибка при создании валюты: {e}")
            raise ValueError(f"Валюта с кодом {currency_data['char_code']} уже существует")

    def _read_currencies(self) -> List[Dict]:
        """Read: чтение всех валют"""
        try:
            sql = "SELECT * FROM currency ORDER BY char_code"
            cursor = self.connection.execute(sql)
            results = [dict(row) for row in cursor.fetchall()]
            logger.debug(f"Прочитано {len(results)} валют")
            return results
        except sqlite3.Error as e:
            logger.error(f"Ошибка при чтении валют: {e}")
            return []

    def _read_currency_by_id(self, currency_id: int) -> Dict:
        """Read: чтение валюты по ID с параметризованным запросом"""
        try:
            sql = "SELECT * FROM currency WHERE id = ?"
            cursor = self.connection.execute(sql, (currency_id,))
            result = cursor.fetchone()
            if result:
                logger.debug(f"Найдена валюта с ID {currency_id}")
                return dict(result)
            logger.debug(f"Валюта с ID {currency_id} не найдена")
            return {}
        except sqlite3.Error as e:
            logger.error(f"Ошибка при чтении валюты: {e}")
            return {}

    def _read_currency_by_char_code(self, char_code: str) -> Dict:
        """Read: чтение валюты по символьному коду"""
        try:
            sql = "SELECT * FROM currency WHERE char_code = ?"
            cursor = self.connection.execute(sql, (char_code,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            return {}
        except sqlite3.Error as e:
            logger.error(f"Ошибка при чтении валюты по коду: {e}")
            return {}

    def _update_currency(self, char_code: str, value: float) -> bool:
        """Update: обновление курса валюты по символьному коду"""
        try:
            sql = "UPDATE currency SET value = ? WHERE char_code = ?"
            cursor = self.connection.execute(sql, (value, char_code))
            self.connection.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Обновлен курс {char_code}: {value}")
            else:
                logger.warning(f"Валюта {char_code} не найдена для обновления")
            return success
        except sqlite3.Error as e:
            logger.error(f"Ошибка при обновлении валюты: {e}")
            return False

    def _delete_currency(self, currency_id: int) -> bool:
        """Delete: удаление валюты по ID"""
        try:
            sql = "DELETE FROM currency WHERE id = ?"
            cursor = self.connection.execute(sql, (currency_id,))
            self.connection.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Удалена валюта с ID {currency_id}")
            else:
                logger.warning(f"Валюта с ID {currency_id} не найдена для удаления")
            return success
        except sqlite3.Error as e:
            logger.error(f"Ошибка при удалении валюты: {e}")
            return False

    def _read_users(self) -> List[Dict]:
        """Read: чтение всех пользователей"""
        try:
            sql = "SELECT * FROM user ORDER BY name"
            cursor = self.connection.execute(sql)
            results = [dict(row) for row in cursor.fetchall()]
            return results
        except sqlite3.Error as e:
            logger.error(f"Ошибка при чтении пользователей: {e}")
            return []

    def _read_user_by_id(self, user_id: int) -> Dict:
        """Read: чтение пользователя по ID"""
        try:
            sql = "SELECT * FROM user WHERE id = ?"
            cursor = self.connection.execute(sql, (user_id,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            return {}
        except sqlite3.Error as e:
            logger.error(f"Ошибка при чтении пользователя: {e}")
            return {}

    def _read_user_currencies(self, user_id: int) -> List[Dict]:
        """Read: чтение валют пользователя с JOIN"""
        try:
            sql = """
                SELECT c.* FROM currency c
                JOIN user_currency uc ON c.id = uc.currency_id
                WHERE uc.user_id = ?
                ORDER BY c.char_code
            """
            cursor = self.connection.execute(sql, (user_id,))
            results = [dict(row) for row in cursor.fetchall()]
            return results
        except sqlite3.Error as e:
            logger.error(f"Ошибка при чтении валют пользователя: {e}")
            return []

    def _create_user(self, name: str) -> int:
        """Create: добавление нового пользователя"""
        try:
            sql = "INSERT INTO user(name) VALUES(?)"
            cursor = self.connection.execute(sql, (name,))
            self.connection.commit()
            logger.info(f"Создан пользователь: {name}")
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Пользователь с именем {name} уже существует")

    def _subscribe_user_to_currency(self, user_id: int, currency_id: int) -> bool:
        """Добавление подписки пользователя на валюту"""
        try:
            sql = "INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)"
            self.connection.execute(sql, (user_id, currency_id))
            self.connection.commit()
            logger.info(f"Пользователь {user_id} подписан на валюту {currency_id}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Пользователь {user_id} уже подписан на валюту {currency_id}")
            return False
        except sqlite3.Error as e:
            logger.error(f"Ошибка при подписке: {e}")
            return False

    def _unsubscribe_user_from_currency(self, user_id: int, currency_id: int) -> bool:
        """Удаление подписки пользователя от валюты"""
        try:
            sql = "DELETE FROM user_currency WHERE user_id = ? AND currency_id = ?"
            cursor = self.connection.execute(sql, (user_id, currency_id))
            self.connection.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Пользователь {user_id} отписан от валюты {currency_id}")
            else:
                logger.warning(f"Подписка пользователя {user_id} на валюту {currency_id} не найдена")
            return success
        except sqlite3.Error as e:
            logger.error(f"Ошибка при отписке: {e}")
            return False

    def _read_all_currencies_for_user(self, user_id: int) -> List[Dict]:
        """Чтение всех валют с информацией о подписке пользователя"""
        try:
            sql = """
                SELECT c.*,
                       CASE WHEN uc.id IS NOT NULL THEN 1 ELSE 0 END as subscribed
                FROM currency c
                LEFT JOIN user_currency uc ON c.id = uc.currency_id AND uc.user_id = ?
                ORDER BY c.char_code
            """
            cursor = self.connection.execute(sql, (user_id,))
            results = [dict(row) for row in cursor.fetchall()]
            return results
        except sqlite3.Error as e:
            logger.error(f"Ошибка при чтении валют для пользователя: {e}")
            return []

    def close(self):
        """Закрытие соединения с БД"""
        if self.connection:
            self.connection.close()
            logger.info("Соединение с БД закрыто")

    def __del__(self):
        """Деструктор для автоматического закрытия соединения"""
        self.close()