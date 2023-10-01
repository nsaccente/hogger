from enum import IntFlag
from math import log2
from pydantic import FieldValidationInfo
from typing import Any, get_args, get_type_hints
from difflib import SequenceMatcher

from inspect import cleandoc
from enum import Enum


class EnumUtils:
    class InvalidEnumValue(Exception):
        def __init__(
            self, 
            field_name: str,
            EnumType: type,
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
    def parse_enum(cls, v: (str | int), info: FieldValidationInfo) -> Enum | int:
        EnumType = list(
            filter(
                lambda field_type: (issubclass(field_type, Enum)),
                get_args(get_type_hints(cls)[info.field_name]),
            )
        )[0]
        enum_domain = {i.name: i.value for i in EnumType}
        suggestion = None
        if issubclass(type(v), Enum):
            return v
        elif isinstance(v, int):
            if v in enum_domain.values():
                return EnumType(v)
            return v
        elif isinstance(v, str):
            if v in enum_domain:
                return EnumType[v]

            # Attempt to find the nearest valid Enum value
            for k in enum_domain.keys():
                if SequenceMatcher(None, v, k).ratio() >= 0.7:
                    suggestion = k
                    break

        raise EnumUtils.InvalidEnumValue(
            field_name=info.field_name,
            EnumType=EnumType,
            expected_values=list(enum_domain.keys()),
            actual=v,
            suggestion=suggestion,
        )


class IntFlagUtils:
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def add_flags(flags: list[int | IntFlag]) -> int:
        return sum([2**flag for flag in flags])

    @staticmethod
    def decompose_int(x: int) -> list[int | IntFlag]:
        powers = []
        i = 1
        while i <= x:
            if i & x:
                powers.append(int(log2(i)))
            i <<= 1
        return powers