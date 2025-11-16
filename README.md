## Employee Directory Console App

Console application for managing an employee directory with multiple execution modes per assignment requirements. Implemented in Python with SQLite (stdlib only).

All text files are UTF-8 encoded.

### Features
- Create table with fields: Last Name, First Name, Middle Name (optional), Birth Date, Gender.
- Add a single employee via CLI.
- List unique employees by FullName + BirthDate, sorted by name, showing age.
- Generate and batch-insert 1,000,000 random employees (+100 forced Male with last name starting with "F").
- Execute and time a filtered query (Male and last name starts with "F").
- Apply DB optimization (indexes) and show timing before/after.

### Tech Stack
- Python 3.10+
- SQLite (`sqlite3` from Python standard library)
- Object-oriented design: `DBManager`, `Employee`

### Project Structure
```
Task_2/
  main.py
  src/
    __init__.py
    db.py        # DBManager: connection, DDL, inserts, queries, indexes
    models.py    # Employee: age calculation, saving, batch insert
    utils.py     # Data generators for bulk mode
  data/
    employees.sqlite  # created on first run
```

### Setup
- Python 3.10+ is required.
- No external dependencies.
- Optional (recommended): create a virtual environment.

Windows PowerShell:
```
cd "C:\Users\amiri\PycharmProjects\Task_2"
python --version
# If needed:
# py --version
```

### Usage (CLI Modes)
- 1) Create table:
```
python main.py 1
```

- 2) Insert one record:
```
python main.py 2 "Ivanov Petr Sergeevich" 2009-07-12 Male
```

- 3) List unique by FullName+BirthDate, sorted; print age:
```
python main.py 3
```

- 4) Generate 1,000,000 records (+100 Male with last name starting 'F') and batch-insert:
```
python main.py 4
```
Note: This may take time and disk space.

- 5) Timed query: gender=Male and last_name starts with 'F':
```
python main.py 5
```
Output example:
```
Query returned 12345 rows in 78.12 ms
```
Use this time in the assignment report.

- 6) Optimization (indexes) + re-run timing:
```
python main.py 6
```
Output example:
```
Baseline: 12345 rows in 78.12 ms
Optimized: 12345 rows in 12.34 ms
Improvement: 65.78 ms faster
```
Include both before/after timings in the report.

### Data Model
Table: `employees`
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `last_name` TEXT NOT NULL
- `first_name` TEXT NOT NULL
- `middle_name` TEXT NULL
- `birth_date` DATE NOT NULL (YYYY-MM-DD)
- `gender` TEXT NOT NULL ("Male" | "Female")

Indexes:
- `idx_employees_name (last_name, first_name, middle_name)` for sorting in mode 3.
- `idx_employees_gender_lastname (gender, last_name)` for filtering in mode 5/6.

### Design Notes
- Age is calculated as full years based on current date and `birth_date`.
- Unique listing (mode 3) deduplicates by `(last_name, first_name, middle_name, birth_date)` using a CTE.
- Bulk insert (mode 4) uses a transaction with `executemany` and relaxed pragmas for speed.

### Troubleshooting
- Start over with an empty DB by deleting `data\employees.sqlite`.
- If `python` is not found, use `py` instead.
- If mode 3 fails on date parsing, ensure you are on the latest code version (dates are now parsed from ISO strings).

### License
MIT



