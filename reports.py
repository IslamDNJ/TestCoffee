"""Регистрация и идентификация отчетов.

Чтобы добавить новый отчет:
1. Определите функцию, которая принимает list[dict] и возвращает list[dict].
2. Зарегистрируйте ее в REPORTS dict с помощью уникального ключа.
"""

from statistics import median

# Registry: report name -> callable(rows) -> list[dict]
REPORTS: dict = {}


def register(name: str):
    """Декоратор для регистрации функции отчета."""

    def decorator(fn):
        REPORTS[name] = fn
        return fn

    return decorator


@register("median-coffee")
def median_coffee(rows: list[dict]) -> list[dict]:
    """Средние расходы на кофе на одного студента, отсортированные по убыванию."""
    spending: dict[str, list[float]] = {}
    for row in rows:
        student = row["student"]
        amount = float(row["coffee_spent"])
        spending.setdefault(student, []).append(amount)

    result = [
        {"student": student, "median_coffee_spent": median(amounts)}
        for student, amounts in spending.items()
    ]
    result.sort(key=lambda x: x["median_coffee_spent"], reverse=True)
    return result
