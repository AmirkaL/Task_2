import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Iterable, List, Optional, Sequence, Tuple


@dataclass
class DBManager:
    db_path: str

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA encoding = 'UTF-8';")
        return conn

    @contextmanager
    def get_connection(self) -> Iterable[sqlite3.Connection]:
        conn = self._connect()
        try:
            yield conn
        finally:
            conn.close()

    def create_table(self) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    middle_name TEXT,
                    birth_date DATE NOT NULL,
                    gender TEXT NOT NULL
                );
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_employees_name ON employees(last_name, first_name, middle_name);"
            )
            conn.commit()

    def insert_one(self, last_name: str, first_name: str, middle_name: Optional[str], birth_date: str, gender: str) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO employees (last_name, first_name, middle_name, birth_date, gender)
                VALUES (?, ?, ?, ?, ?);
                """,
                (last_name, first_name, middle_name, birth_date, gender),
            )
            conn.commit()

    def insert_many(self, rows: Sequence[Tuple[str, str, Optional[str], str, str]]) -> None:
        with self.get_connection() as conn:
            conn.execute("PRAGMA synchronous = OFF;")
            conn.execute("PRAGMA journal_mode = MEMORY;")
            conn.execute("BEGIN TRANSACTION;")
            conn.executemany(
                """
                INSERT INTO employees (last_name, first_name, middle_name, birth_date, gender)
                VALUES (?, ?, ?, ?, ?);
                """,
                rows,
            )
            conn.commit()

    def fetch_unique_sorted(self) -> List[Tuple[str, str, Optional[str], str, str]]:
        with self.get_connection() as conn:
            cur = conn.execute(
                """
                WITH uniq AS (
                    SELECT MIN(id) AS id
                    FROM employees
                    GROUP BY last_name, first_name, middle_name, birth_date
                )
                SELECT e.last_name, e.first_name, e.middle_name, e.birth_date, e.gender
                FROM employees e
                JOIN uniq u ON u.id = e.id
                ORDER BY e.last_name, e.first_name, e.middle_name;
                """
            )
            return [(r[0], r[1], r[2], r[3], r[4]) for r in cur.fetchall()]

    def query_male_lastname_f_with_timing(self) -> Tuple[float, int]:
        with self.get_connection() as conn:
            start = perf_counter()
            cur = conn.execute(
                """
                SELECT COUNT(*)
                FROM employees
                WHERE gender = 'Male'
                  AND last_name LIKE 'F%';
                """
            )
            count = cur.fetchone()[0]
            elapsed_ms = (perf_counter() - start) * 1000.0
            return elapsed_ms, count

    def create_optimization_indexes(self) -> None:
        with self.get_connection() as conn:
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_employees_gender_lastname ON employees(gender, last_name);"
            )
            conn.commit()



