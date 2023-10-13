from difflib import SequenceMatcher
from enum import Enum
from typing import get_args, get_type_hints

from pydantic import FieldSerializationInfo, FieldValidationInfo

from .errors import InvalidValueException


class EnumUtils:
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

        raise InvalidValueException(
            field_name=info.field_name,
            expected_values=list(domain.keys()),
            FieldType=Enum,
            actual=v,
            suggestion=suggestion,
        )

    @staticmethod
    def serialize(self, v: (Enum | int), info: FieldSerializationInfo) -> str | int:
        if isinstance(v, int):
            return v
        return v.name