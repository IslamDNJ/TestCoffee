"""Скрипт для создания отчетов о данных подготовки студентов к экзаменам."""

import argparse
import csv
import sys
from pathlib import Path

from tabulate import tabulate

from reports import REPORTS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Создание отчетов на основе данных о подготовке студентов к экзаменам."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        metavar="FILE",
        help="Пути к файлам CSV",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=list(REPORTS.keys()),
        help=f"Report type. Available: {', '.join(REPORTS.keys())}",
    )
    return parser.parse_args()


def read_csv_files(file_paths: list[str]) -> list[dict]:
    rows = []
    for path_str in file_paths:
        path = Path(path_str)
        if not path.exists():
            print(f"Error: file not found: {path_str}", file=sys.stderr)
            sys.exit(1)
        if not path.is_file():
            print(f"Error: not a file: {path_str}", file=sys.stderr)
            sys.exit(1)
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows.extend(reader)
    return rows


def main() -> None:
    args = parse_args()
    rows = read_csv_files(args.files)

    report_fn = REPORTS[args.report]
    result = report_fn(rows)

    print(tabulate(result, headers="keys", tablefmt="simple"))


if __name__ == "__main__":
    main()
