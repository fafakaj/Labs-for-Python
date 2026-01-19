# Лабораторная работа: Клиент-серверное приложение на Python

### Основные задачи

**CRUD для Currency:**
- Create - добавление новых валют через API
- Read - вывод всех валют из базы данных
- Update - обновление курсов валют из API ЦБ РФ
- Delete - удаление валют по ID

**Работа с SQLite:**
- Используется база данных в памяти (`:memory:`)
- Первичные ключи (PRIMARY KEY) для уникальной идентификации записей
- Внешние ключи (FOREIGN KEY) для связей между таблицами user и currency через user_currency


### Контроллеры и MVC

**Архитектура MVC реализована:**
- **Models** (`models/currency.py`) - свойства сущностей, геттеры/сеттеры
- **Controllers** - разделены на модули:
  - `databasecontroller.py` - работа с SQLite
  - `currencycontroller.py` - бизнес-логика
  - `pages.py` - рендеринг через Jinja2
- **Views** - HTML шаблоны в `templates/`

### Роутер и функциональность

**Маршруты реализованы:**
- `/` - главная страница
- `/author` - информация об авторе
- `/users` - список пользователей
- `/user?id=X` - страница пользователя
- `/currencies` - список валют
- `/currency/delete?id=X` - удаление валюты
- `/currency/add` - добавление валюты
- `/currency/update_all` - обновление всех курсов

**Дополнительные возможности:**
- Подписки пользователей на валюты
- Графики курсов валют за 4 месяца
- Параметризованные запросы для защиты от SQL-инъекций

### Тестирование

в папке `tests/`:**

**Тесты с unittest.mock:**
1. `test_list_currencies` - чтение списка валют
2. `test_create_currency` - создание новой валюты
3. `test_delete_currency` - удаление валюты

**Тесты:**
1. `test_currency_creation` - создание объекта Currency
2. `test_currency_validation` - валидация данных модели
3. `test_route_structure` - проверка маршрутов приложения

**Пример теста с mock:**
```python
def test_list_currencies(self):
    self.mock_db._read_currencies.return_value = [{"id": 1, "char_code": "USD"}]
    result = self.controller.list_currencies()
    self.assertEqual(result[0]['char_code'], "USD")
    self.mock_db._read_currencies.assert_called_once()
```

## Структура проекта

```
pylab9/
├── __init__.py
├── controllers/
│   ├── __init__.py
│   ├── currencycontroller.py
│   ├── databasecontroller.py
│   ├── main_controller.py
│   └── pages.py
├── models/
│   ├── __init__.py
│   ├── currency.py
│   └── user.py
├── services/
│   ├── __init__.py
│   └── currencies_api.py
├── templates/
│   ├── author.html
│   ├── currencies.html
│   ├── index.html
│   ├── user_charts.html
│   ├── user.html
│   └── users.html
├── tests/
│   ├── __init__.py
│   ├── test_currency_controller.py
│   ├── test_currency_model.py
│   └── test_main_controller.py
├── myapp.py
└── README.md
```

## Выводы

В результате выполнения лабораторной работы была создана полнофункциональная веб-приложение для отслеживания курсов валют с использованием архитектуры MVC. Приложение демонстрирует:

1. **Работу с SQLite** - создание таблиц с первичными и внешними ключами, параметризованные запросы
2. **MVC архитектуру** - четкое разделение ответственности между моделями, контроллерами и представлениями
3. **Обработку HTTP запросов** - роутинг, параметры запросов, редиректы
4. **Рендеринг шаблонов** - использование Jinja2 для динамических страниц
5. **Тестирование** - использование unittest.mock для изоляции зависимостей

## Примеры работы
<img width="1062" height="418" alt="image" src="https://github.com/user-attachments/assets/4a4fb5e0-8e80-40cf-be2a-86d2e8eba698" />
<img width="1280" height="470" alt="image" src="https://github.com/user-attachments/assets/59e56e2e-54e4-402c-8ec4-9a6b09b5e09c" />
<img width="1280" height="470" alt="image" src="https://github.com/user-attachments/assets/4393422b-8e09-4f58-a5a7-8e74f6fde689" />
<img width="1280" height="470" alt="image" src="https://github.com/user-attachments/assets/b0c23959-dc1a-4ce2-b809-f42135aa2270" />
<img width="1280" height="616" alt="image" src="https://github.com/user-attachments/assets/d0c28ae1-aa77-4665-b527-11389ce83b4c" />
<img width="1280" height="616" alt="image" src="https://github.com/user-attachments/assets/538f4f9c-47ff-43e6-8846-2c28560f9855" />
<img width="1280" height="351" alt="image" src="https://github.com/user-attachments/assets/af0f3283-27d7-44af-9646-dc22f9fe6f28" />



