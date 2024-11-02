from dataclasses import dataclass
import datetime

from . import validator


@dataclass()
class Lesson(validator.Validations):
    date: str
    day: str
    time: str
    number: int
    subject: str
    lesson_type: str
    location: str
    teacher: str

    def date_to_datetime(self):
        self.date = datetime.datetime.strptime(self.date, "%Y-%m-%d")

    def validate_number(self, value, **_) -> int:
        if isinstance(value, str):
            value = int(value)
        return value
