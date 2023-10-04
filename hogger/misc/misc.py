from typing import Optional

from pydantic import BaseModel, Field, model_serializer, SerializationInfo

LookupID = int


class Money(BaseModel):
    gold: int = Field(default=0, ge=0)
    silver: int = Field(default=0, ge=0)
    copper: int = Field(default=0, ge=0)

    def to_copper(self) -> int:
        return (self.copper) + (self.silver * 100) + (10000 * self.gold)

    @staticmethod
    def from_copper(c: int) -> "Money":
        copper: int = c % 100
        c = (c - copper) / 100
        silver: int = c % 100
        gold: int = (c - silver) / 100
        return Money(
            gold=gold,
            silver=silver,
            copper=copper,
        )


# Why is Time in `currency.py`? Because "Time is money, friend."
class Duration(BaseModel):
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milli: int = 0

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def to_seconds(self) -> int:
        return sum(
            [
                (self.days * 86400),
                (self.hours * 3600),
                (self.minutes * 60),
                (self.seconds),
            ]
        )

    def to_milli(self) -> int:
        return sum([(self.to_seconds * 1000), self.milli])
