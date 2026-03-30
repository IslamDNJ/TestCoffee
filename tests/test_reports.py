"""Тесты для проекта."""

import pytest

from reports import median_coffee, REPORTS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def single_student_rows():
    # Иван Кузнецов, Математика
    return [
        {"student": "Иван Кузнецов", "coffee_spent": "600"},
        {"student": "Иван Кузнецов", "coffee_spent": "650"},
        {"student": "Иван Кузнецов", "coffee_spent": "700"},
    ]


@pytest.fixture
def multi_student_rows():
    # Данные из math.csv для трёх студентов
    return [
        {"student": "Алексей Смирнов", "coffee_spent": "450"},
        {"student": "Алексей Смирнов", "coffee_spent": "500"},
        {"student": "Алексей Смирнов", "coffee_spent": "550"},
        {"student": "Дарья Петрова", "coffee_spent": "200"},
        {"student": "Дарья Петрова", "coffee_spent": "250"},
        {"student": "Дарья Петрова", "coffee_spent": "300"},
        {"student": "Иван Кузнецов", "coffee_spent": "600"},
        {"student": "Иван Кузнецов", "coffee_spent": "650"},
        {"student": "Иван Кузнецов", "coffee_spent": "700"},
    ]


# ---------------------------------------------------------------------------
# median_coffee report
# ---------------------------------------------------------------------------

class TestMedianCoffee:
    def test_single_student_odd_count(self, single_student_rows):
        result = median_coffee(single_student_rows)
        assert len(result) == 1
        assert result[0]["student"] == "Иван Кузнецов"
        assert result[0]["median_coffee_spent"] == 650.0

    def test_single_student_even_count(self):
        rows = [
            {"student": "Иван", "coffee_spent": "100"},
            {"student": "Иван", "coffee_spent": "200"},
        ]
        result = median_coffee(rows)
        assert result[0]["median_coffee_spent"] == 150.0

    def test_multiple_students_sorted_descending(self, multi_student_rows):
        result = median_coffee(multi_student_rows)
        medians = [r["median_coffee_spent"] for r in result]
        assert medians == sorted(medians, reverse=True)

    def test_multiple_students_correct_values(self, multi_student_rows):
        result = median_coffee(multi_student_rows)
        by_name = {r["student"]: r["median_coffee_spent"] for r in result}
        assert by_name["Алексей Смирнов"] == 500.0
        assert by_name["Дарья Петрова"] == 250.0
        assert by_name["Иван Кузнецов"] == 650.0

    def test_result_contains_required_keys(self, multi_student_rows):
        result = median_coffee(multi_student_rows)
        for row in result:
            assert "student" in row
            assert "median_coffee_spent" in row

    def test_single_entry_per_student(self):
        rows = [{"student": "Мария Соколова", "coffee_spent": "120"}]
        result = median_coffee(rows)
        assert len(result) == 1
        assert result[0]["median_coffee_spent"] == 120.0

    def test_data_from_multiple_files_aggregated(self):
        """Rows from two 'files' should be combined before computing median."""
        # Алексей Смирнов across math.csv and physics.csv
        file1 = [
            {"student": "Алексей Смирнов", "coffee_spent": "450"},
            {"student": "Алексей Смирнов", "coffee_spent": "500"},
            {"student": "Алексей Смирнов", "coffee_spent": "550"},
        ]
        file2 = [
            {"student": "Алексей Смирнов", "coffee_spent": "480"},
            {"student": "Алексей Смирнов", "coffee_spent": "530"},
            {"student": "Алексей Смирнов", "coffee_spent": "580"},
        ]
        result = median_coffee(file1 + file2)
        assert len(result) == 1
        assert result[0]["median_coffee_spent"] == 515.0  # median of [450,480,500,530,550,580]


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class TestReportsRegistry:
    def test_median_coffee_registered(self):
        assert "median-coffee" in REPORTS

    def test_registered_callable(self):
        assert callable(REPORTS["median-coffee"])

    def test_registered_function_is_median_coffee(self):
        assert REPORTS["median-coffee"] is median_coffee


# ---------------------------------------------------------------------------
# Integration: read_csv_files
# ---------------------------------------------------------------------------

class TestReadCsvFiles:
    def test_reads_existing_file(self, tmp_path):
        from main import read_csv_files

        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
            "Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика\n",
            encoding="utf-8",
        )
        rows = read_csv_files([str(csv_file)])
        assert len(rows) == 1
        assert rows[0]["student"] == "Иван Кузнецов"
        assert rows[0]["coffee_spent"] == "600"

    def test_raises_on_missing_file(self):
        from main import read_csv_files
        import sys

        with pytest.raises(SystemExit):
            read_csv_files(["/nonexistent/path/file.csv"])

    def test_merges_multiple_files(self, tmp_path):
        from main import read_csv_files

        header = "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        f1 = tmp_path / "math.csv"
        f1.write_text(header + "Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика\n", encoding="utf-8")
        f2 = tmp_path / "physics.csv"
        f2.write_text(header + "Дарья Петрова,2024-06-06,280,6.5,7,норм,Физика\n", encoding="utf-8")

        rows = read_csv_files([str(f1), str(f2)])
        assert len(rows) == 2
        students = {r["student"] for r in rows}
        assert students == {"Иван Кузнецов", "Дарья Петрова"}