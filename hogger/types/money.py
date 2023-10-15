from pydantic import BaseModel, Field
from mysql.connector.cursor_cext import CMySQLCursor as Cursor

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

    @staticmethod
    def from_sql_copper(field: str):
        def from_sql_copper(
            sql_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> "Money":
            return Money.from_copper(sql_dict[field])
        return from_sql_copper