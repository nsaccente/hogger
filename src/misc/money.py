from typing import Optional

from pydantic import BaseModel, Field


class Money(BaseModel):
    gold: Optional[int]
    silver: Optional[int]
    copper: Optional[int]

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
