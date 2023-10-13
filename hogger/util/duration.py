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
            ]
        )

    def to_milli(self) -> int:
        return sum([(self.to_seconds * 1000), self.milli])
    

    @staticmethod
    def from_seconds(s) -> "Duration":
        seconds_to_minute   = 60
        seconds_to_hour     = 60 * seconds_to_minute
        seconds_to_day      = 24 * seconds_to_hour

        days = s // seconds_to_day
        s %= seconds_to_day

        hours = s // seconds_to_hour
        s %= seconds_to_hour

        minutes = s // seconds_to_minute
        s %= seconds_to_minute

        seconds = s  

        return Duration(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milli=0,
        )


    @staticmethod
    def from_sql_seconds(field: str):
        def from_sql_seconds(sql_dict: dict[str, any]) -> Duration:
            return Duration.from_seconds(sql_dict[field])
        return from_sql_seconds
