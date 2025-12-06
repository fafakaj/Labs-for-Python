# Лабораторная работа: Логирование и декораторы

## Отчёт

В рамках задания реализованы следующие компоненты:

### 1. Исходные файлы

- **Декоратор с параметрами** — `Logger.py`  
- **Функция получения курсов валют** — `Currency.py`  
- **Демонстрационный пример (квадратное уравнение)** — `Demo.py`  
- **Тесты** — `Tests.py`

---

### 2. Фрагменты логов

#### Получение курсов валют (`get_currencies`):
[INFO] Вызов get_currencies c args = (['USD', 'EUR'],), kwargs = {}
[INFO] get_currencies вернула {'USD': 76.0937, 'EUR': 88.7028}
Результат: {'USD': 76.0937, 'EUR': 88.7028}

#### Решение квадратного уравнения (`solve_quadratic`):

- **INFO: два корня**  
2025-12-05 21:05:21,267 - quadratic - INFO - Вызов solve_quadratic c args = (1, -5, 6), kwargs = {}
  2025-12-05 21:05:21,267 - quadratic - INFO - solve_quadratic: Два корня, корни: [3.0, 2.0]


- **WARNING: дискриминант < 0**  
2025-12-05 21:05:21,268 - quadratic - INFO - Вызов solve_quadratic c args = (1, 0, 1), kwargs = {}
  2025-12-05 21:05:21,268 - quadratic - WARNING - solve_quadratic: Дискриминант < 0 (-4), нет действительных корней

- **ERROR: некорректные данные**  
2025-12-05 21:05:21,268 - quadratic - INFO - Вызов solve_quadratic c args = ('abc', 1, 1), kwargs = {}
  2025-12-05 21:05:21,268 - quadratic - ERROR - solve_quadratic выбросила TypeError: Все коэффициенты должны быть числами, получено: a=<class 'str'>, b=<class 'int'>, c=<class 'int'>
  Перехвачено исключение: Все коэффициенты должны быть числами, получено: a=<class 'str'>, b=<class 'int'>, c=<class 'int'>

- **CRITICAL: вырожденное уравнение**  
2025-12-05 21:05:21,268 - quadratic - INFO - Вызов solve_quadratic c args = (0, 0, 5), kwargs = {}
  2025-12-05 21:05:21,268 - quadratic - CRITICAL - solve_quadratic: Нет решений (5 = 0

#### Файловое логирование (`currency.log`):
Чтобы запустить логгирование нужно прописат: python FULL.py demo
Результат: {'USD': 76.0937}
Логи записаны в файл currency.log

---

### 3. Тестирование

Все тесты реализованы в файле **`Tests.py`** и охватывают:

- **Тесты функции `get_currencies`**:  
  - Успешное получение курсов  
  - Обработка `ConnectionError`, `ValueError`, `KeyError`, `TypeError`

- **Тесты декоратора `@logger`**:  
  - Логирование в `sys.stdout`  
  - Логирование в файл через `logging.Logger`  
  - Обработка исключений

- **Тесты работы с `StringIO`**:  
  - Проверка перехвата вывода в память для unit-тестов

Все тесты проходят успешно.
