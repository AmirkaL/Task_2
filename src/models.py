from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional, Sequence, Tuple

from .db import DBManager


def _normalize_gender(value: str) -> str:
    normalized = value.strip().capitalize()
    if normalized not in {"Male", "Female"}:
        raise ValueError("Gender must be 'Male' or 'Female'")
    return normalized


def _split_full_name(full_name: str) -> Tuple[str, str, Optional[str]]:
    parts = [p for p in full_name.strip().split() if p]
    if len(parts) < 2:
        raise ValueError("Full name must contain at least LastName and FirstName")
    if len(parts) == 2:
        last_name, first_name = parts[0], parts[1]
        middle_name = None
    else:
        last_name, first_name = parts[0], parts[1]
        middle_name = " ".join(parts[2:])
    return last_name, first_name, middle_name


@dataclass
class Employee:
    last_name: str
    first_name: str
    middle_name: Optional[str]
    birth_date: date
    gender: str

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    @property
    def age_years(self) -> int:
        today = date.today()
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

    def save_to_db(self, db: DBManager) -> None:
        db.insert_one(
            last_name=self.last_name,
            first_name=self.first_name,
            middle_name=self.middle_name,
            birth_date=self.birth_date.isoformat(),
            gender=self.gender,
        )

    @classmethod
    def batch_insert(cls, db: DBManager, employees: Sequence["Employee"]) -> None:
        rows: List[Tuple[str, str, Optional[str], str, str]] = []
        for e in employees:
            rows.append(
                (e.last_name, e.first_name, e.middle_name, e.birth_date.isoformat(), e.gender)
            )
        db.insert_many(rows)

    @classmethod
    def from_full_name(cls, full_name: str, birth_date: date, gender: str) -> "Employee":
        last_name, first_name, middle_name = _split_full_name(full_name)
        normalized_gender = _normalize_gender(gender)
        return cls(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            birth_date=birth_date,
            gender=normalized_gender,
        )



