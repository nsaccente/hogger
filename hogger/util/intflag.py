from difflib import SequenceMatcher
from enum import Enum, IntFlag
from typing import get_args, get_type_hints

from pydantic import FieldValidationInfo, SerializationInfo
from mysql.connector.cursor_cext import CMySQLCursor as Cursor

from .errors import InvalidValueException


class IntFlagUtils:
    class InvalidIntFlagValue(Exception):
        def __init__(
            self,
            field_name: str,
            expected_values: list[str],
            actual: any,
            suggestion: any = None,
        ) -> None:
            e = (
                f"Invalid value for IntFlag field '{field_name}'; valid values are "
                f"{expected_values}, or an integer, got '{actual}'"
            )
            if suggestion is not None:
                e += f".\n\nDid you mean '{suggestion}' for field '{field_name}'?"
            super().__init__(e)


    @staticmethod
    def parse(
        cls, items: list[str | int], info: FieldValidationInfo
    ) -> list[IntFlag | int]:
        IntFlagType = (
            list(
                filter(
                    lambda field_type: (issubclass(field_type, Enum)),
                    get_args(get_args(get_type_hints(cls)[info.field_name])[0]),
                )
            )
        )[0]
        domain = {i.name: i.value for i in IntFlagType}
        result = []
        suggestion = None
        try:
            for item in items:
                if isinstance(item, IntFlagType):
                    result.append(item)
                elif isinstance(item, int):
                    flag = 2**item
                    if flag in domain.values():
                        result.append(IntFlagType(flag))
                    else:
                        result.append(item)
                elif isinstance(item, str):
                    if item in domain:
                        result.append(IntFlagType[item])
                    else:
                        # Attempt to find the nearest valid Enum value
                        for k in domain.keys():
                            if SequenceMatcher(None, item, k).ratio() >= 0.7:
                                suggestion = k
                                raise
            return list(set(result))
        except:
            raise InvalidValueException(
                field_name=info.field_name,
                expected_values=list(domain.keys()),
                FieldType=IntFlag,
                actual=item,
                suggestion=suggestion,
            )


    def serialize(
        self, items: list[int | IntFlag], info: SerializationInfo
    ) -> list[str | int]:
        result = []
        for item in items:
            if issubclass(type(item), IntFlag):
                result.append(item.name)
            else:
                result.append(item)
        return result

    @staticmethod
    def from_sql(field: str):
        def from_sql(
            sql_dict: dict[str, any], 
            cursor: Cursor,
            field_type: type,
        ) -> IntFlag:
            for t in get_args(get_args(field_type)[0]):
                if issubclass(t, IntFlag):
                    IntFlagType = t
                    break

            if sql_dict[field] == -1:
                flags = []
            else:
                flags = [flag for flag in IntFlagType if flag in IntFlagType(sql_dict[field])]
            return flags
        return from_sql