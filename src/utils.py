import random
from datetime import date, timedelta
from typing import List

from .models import Employee


MALE_FIRST_NAMES = [
    "Ivan", "Petr", "Sergey", "Alexey", "Dmitry", "Andrey", "Mikhail", "Nikolay", "Yuri", "Victor",
]
FEMALE_FIRST_NAMES = [
    "Anna", "Maria", "Elena", "Olga", "Irina", "Tatiana", "Svetlana", "Natalia", "Ekaterina", "Alina",
]

LAST_NAME_LETTERS = [chr(c) for c in range(ord("A"), ord("Z") + 1)]

LAST_NAME_SUFFIXES_MALE = ["ov", "ev", "in", "sky", "ko", "ich", "en", "ian", "son", "man"]
LAST_NAME_SUFFIXES_FEMALE = ["ova", "eva", "ina", "skaya", "ko", "ich", "en", "ian", "son", "man"]

MIDDLE_NAME_PARTS = ["Petrov", "Ivanov", "Sergeev", "Alexeev", "Dmitriev", "Andreev", "Mikhailov"]


def random_birth_date(min_age: int = 18, max_age: int = 65) -> date:
    today = date.today()
    start = today.replace(year=today.year - max_age)
    end = today.replace(year=today.year - min_age)
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def random_last_name(gender: str, first_letter: str | None = None) -> str:
    letter = first_letter if first_letter else random.choice(LAST_NAME_LETTERS)
    if gender == "Male":
        suffix = random.choice(LAST_NAME_SUFFIXES_MALE)
    else:
        suffix = random.choice(LAST_NAME_SUFFIXES_FEMALE)
    return f"{letter}{suffix.capitalize()}"


def random_first_name(gender: str) -> str:
    return random.choice(MALE_FIRST_NAMES if gender == "Male" else FEMALE_FIRST_NAMES)


def random_middle_name() -> str:
    base = random.choice(MIDDLE_NAME_PARTS)
    return f"{base}ich"


def generate_employees_bulk(total: int, ensure_f_males: int) -> List[Employee]:
    employees: List[Employee] = []
    genders = ["Male", "Female"]

    letters_cycle = LAST_NAME_LETTERS * ((total // len(LAST_NAME_LETTERS)) + 1)
    random.shuffle(letters_cycle)
    for i in range(total - ensure_f_males):
        gender = random.choice(genders)
        letter = letters_cycle[i]
        last_name = random_last_name(gender, first_letter=letter)
        first_name = random_first_name(gender)
        middle_name = random_middle_name() if random.random() < 0.7 else None
        birth_date = random_birth_date()
        employees.append(
            Employee(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                birth_date=birth_date,
                gender=gender,
            )
        )

    # Ensure required Male + last name starting with 'F'
    for _ in range(ensure_f_males):
        gender = "Male"
        last_name = random_last_name(gender, first_letter="F")
        first_name = random_first_name(gender)
        middle_name = random_middle_name() if random.random() < 0.7 else None
        birth_date = random_birth_date()
        employees.append(
            Employee(
                last_name=last_name,
                first_name=first_name,
                middle_name=middle_name,
                birth_date=birth_date,
                gender=gender,
            )
        )

    random.shuffle(employees)
    return employees



