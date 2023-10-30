from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import BaseModel


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
            ],
        )

    def to_milli(self) -> int:
        return (self.to_seconds() * 1000) + self.milli

    def __int__(self) -> int:
        return self.to_milli()

    @staticmethod
    def from_seconds(s) -> "Duration":
        return Duration.from_milli(s * 1000)

    @staticmethod
    def from_milli(ms) -> "Duration":
        milli_to_second = 1000
        milli_to_minute = 60 * milli_to_second
        milli_to_hour = 60 * milli_to_minute
        milli_to_day = 24 * milli_to_hour

        days = ms // milli_to_day
        ms %= milli_to_day

        hours = ms // milli_to_hour
        ms %= milli_to_hour

        minutes = ms // milli_to_minute
        ms %= milli_to_minute

        seconds = ms // milli_to_second
        ms %= milli_to_second

        milli = ms

        return Duration(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milli=milli,
        )

    @staticmethod
    def from_sql_seconds(field: str):
        def from_sql_seconds(
            sql_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> Duration:
            return Duration.from_seconds(sql_dict[field])

        return from_sql_seconds

    @staticmethod
    def from_sql_milli(field: str):
        def from_sql_seconds(
            sql_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> Duration:
            return Duration.from_milli(sql_dict[field])

        return from_sql_seconds

    @staticmethod
    def to_sql_seconds(sql_field: str):
        def to_sql_seconds(
            model_field: str,
            model_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> dict[str, any]:
            d: Duration = model_dict[model_field]
            return {sql_field: d.to_seconds()}

        return to_sql_seconds
