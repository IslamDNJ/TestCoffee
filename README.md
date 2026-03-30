# Coffee Report

Скрипт формирует отчёты по данным о подготовке студентов к экзаменам из CSV-файлов.

## Создание папки venv
```bash
python -m venv venv
```

## Активация папки venv
```bash
venv\Scripts\activate
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск

```bash
# один файл
python main.py --files data/math.csv --report median-coffee

# все три сессии сразу
python main.py --files data/math.csv data/physics.csv data/programming.csv --report median-coffee
```

## После запуска в терминале:
![Один файл](IMG/1FileUse)

![Все файлы](IMG/AllFileUse.png)

## Тесты

```bash
pytest --cov=. tests/
```

## После запуска в терминале:
![Тесты](IMG/Tests.png)

## Добавление нового отчёта

Зарегистрируйте функцию в `reports.py` через декоратор `@register`:

```python
@register("my-report")
def my_report(rows: list[dict]) -> list[dict]:
    ...
    return [{"column": value, ...}]
```

Новый отчёт сразу доступен через `--report my-report`.

## Пояснение по файловой структуре проекта

Папка data - хранятся .csv файлы для обработки скриптом
Папка tests - множество тестовых описаний для проверки данных
.coveragers - записано исключение для файла main.py и tests/__init.py при вызове тестов
.gitignore - исключения папок/файлов при выгрузке на GitHub
main.py - скрипт для создание отчетов
reports - индентификация и регистрация отчетов
requirements.txt - для pip intsll