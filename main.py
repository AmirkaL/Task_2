import sys
from pathlib import Path
from typing import List
from datetime import datetime

from src.db import DBManager
from src.models import Employee
from src.utils import generate_employees_bulk


def print_usage() -> None:
    print("Usage:")
    print("  python main.py 1")
    print('  python main.py 2 "Ivanov Petr Sergeevich" 2009-07-12 Male')
    print("  python main.py 3")
    print("  python main.py 4")
    print("  python main.py 5")
    print("  python main.py 6")


def mode_1_create_table(db: DBManager) -> None:
    db.create_table()
    print("Table ensured.")


def mode_2_insert_one(db: DBManager, args: List[str]) -> None:
    if len(args) < 3:
        print('Mode 2 requires: "Full Name" YYYY-MM-DD Gender')
        print('Example: python main.py 2 "Ivanov Petr Sergeevich" 2009-07-12 Male')
        return
    full_name = args[0]
    birth_date_str = args[1]
    gender = args[2]
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Expected YYYY-MM-DD.")
        return
    try:
        employee = Employee.from_full_name(full_name=full_name, birth_date=birth_date, gender=gender)
        employee.save_to_db(db)
        print("Inserted 1 employee.")
    except ValueError as e:
        print(f"Error: {e}")


def mode_3_list_unique_sorted(db: DBManager) -> None:
    rows = db.fetch_unique_sorted()
    for row in rows:
        last_name, first_name, middle_name, birth_date, gender = row
        if isinstance(birth_date, str):
            birth_date_obj = datetime.fromisoformat(birth_date).date()
        else:
            birth_date_obj = birth_date
        emp = Employee(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birth_date=birth_date_obj,
            gender=gender,
        )
        print(f"{emp.full_name}\t{birth_date_obj}\t{gender}\t{emp.age_years}")
    print(f"Total: {len(rows)}")


def mode_4_generate_and_insert(db: DBManager) -> None:
    # Generate 1,000,000 with roughly even distribution + 100 males with last name starting with 'F'
    print("Generating employees... This may take a while.")
    employees = generate_employees_bulk(total=1_000_000, ensure_f_males=100)
    print(f"Generated {len(employees)} employees. Inserting in batch...")
    Employee.batch_insert(db, employees)
    print("Batch insert completed.")


def mode_5_query_with_timing(db: DBManager) -> None:
    elapsed_ms, rows = db.query_male_lastname_f_with_timing()
    print(f"Query returned {rows} rows in {elapsed_ms:.2f} ms")


def mode_6_optimize_and_time(db: DBManager) -> None:
    print("Running baseline timing...")
    baseline_ms, baseline_rows = db.query_male_lastname_f_with_timing()
    print(f"Baseline: {baseline_rows} rows in {baseline_ms:.2f} ms")
    print("Applying optimization (indexes)...")
    db.create_optimization_indexes()
    print("Running timing after optimization...")
    optimized_ms, optimized_rows = db.query_male_lastname_f_with_timing()
    print(f"Optimized: {optimized_rows} rows in {optimized_ms:.2f} ms")
    if optimized_ms <= baseline_ms:
        improvement = baseline_ms - optimized_ms
        print(f"Improvement: {improvement:.2f} ms faster")
    else:
        regression = optimized_ms - baseline_ms
        print(f"No improvement. Regression: {regression:.2f} ms slower")


def main() -> None:
    if len(sys.argv) < 2:
        print_usage()
        return
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    db_path = data_dir / "employees.sqlite"
    db = DBManager(db_path=str(db_path))
    mode = sys.argv[1]
    if mode == "1":
        mode_1_create_table(db)
    elif mode == "2":
        mode_2_insert_one(db, sys.argv[2:])
    elif mode == "3":
        mode_3_list_unique_sorted(db)
    elif mode == "4":
        mode_4_generate_and_insert(db)
    elif mode == "5":
        mode_5_query_with_timing(db)
    elif mode == "6":
        mode_6_optimize_and_time(db)
    else:
        print("Unknown mode.")
        print_usage()


if __name__ == "__main__":
    main()



