from enum import IntFlag
from math import log2
from pydantic import FieldValidationInfo, FieldSerializationInfo, SerializationInfo
from typing import Any, get_args, get_type_hints
from difflib import SequenceMatcher

from inspect import cleandoc
from enum import Enum


class EnumUtils:
    class InvalidEnumValue(Exception):
        def __init__(
            self, 
            field_name: str,
            expected_values: list[str],
            actual: Any, 
            suggestion: Any = None,
        ) -> None:
            e = (
                f"Invalid value for Enum field '{field_name}'; valid values are " 
                f"{expected_values}, or an integer, got '{actual}'"
            )
            if suggestion is not None:
                e += f".\n\nDid you mean '{suggestion}' for field '{field_name}'?"
            super().__init__(e)

    @staticmethod
    def parse(cls, v: (str | int), info: FieldValidationInfo) -> Enum | int:
        EnumType = list(
            filter(
                lambda field_type: (issubclass(field_type, Enum)),
                get_args(get_type_hints(cls)[info.field_name]),
            )
        )[0]
        domain = {i.name: i.value for i in EnumType}
        suggestion = None
        if issubclass(type(v), Enum):
            return v
        elif isinstance(v, int):
            if v in domain.values():
                return EnumType(v)
            return v
        elif isinstance(v, str):
            if v in domain:
                return EnumType[v]
            else:
                # Attempt to find the nearest valid Enum value
                for k in domain.keys():
                    if SequenceMatcher(None, v, k).ratio() >= 0.7:
                        suggestion = k
                        break

        raise EnumUtils.InvalidEnumValue(
            field_name=info.field_name,
            expected_values=list(domain.keys()),
            actual=v,
            suggestion=suggestion,
        )

    @staticmethod
    def serialize(self, v: (Enum | int), info: FieldSerializationInfo) -> (str | int):
        if isinstance(v, int):
            return v
        return v.name


class IntFlagUtils:
    class InvalidIntFlagValue(Exception):
        def __init__(
            self, 
            field_name: str,
            expected_values: list[str],
            actual: Any, 
            suggestion: Any = None,
        ) -> None:
            e = (
                f"Invalid value for IntFlag field '{field_name}'; valid values are " 
                f"{expected_values}, or an integer, got '{actual}'"
            )
            if suggestion is not None:
                e += f".\n\nDid you mean '{suggestion}' for field '{field_name}'?"
            super().__init__(e)

    @staticmethod
    def parse(cls, items: list[str | int], info: FieldValidationInfo) -> list[IntFlag | int]:
        IntFlagType = (
            list(
                filter(
                    lambda field_type: (issubclass(field_type, Enum)),
                    get_args(
                        get_args(
                            get_type_hints(cls)[info.field_name]
                        )[0]
                    ),
                )
            )
        )[0]
        domain = {i.name: i.value for i in IntFlagType}
        result = []
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
                    raise IntFlagUtils.InvalidIntFlagValue(
                        field_name=info.field_name,
                        expected_values=list(domain.keys()),
                        actual=item,
                        suggestion=suggestion,
                    )
        return list(set(result))

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