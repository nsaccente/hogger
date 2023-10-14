from difflib import SequenceMatcher
from enum import Enum
from typing import get_args, get_type_hints

from pydantic import SerializationInfo

from .errors import InvalidValueException


class EnumMapUtils:
    @staticmethod
    def parse(
        cls, dmap: dict[(str | int), int], info: SerializationInfo
    ) -> dict[(Enum | int), int]:
        EnumKeyType = (
            list(
                filter(
                    lambda field_type: (issubclass(field_type, Enum)),
                    get_args(get_args(get_type_hints(cls)[info.field_name])[0]),
                )
            )
        )[0]

        domain = {i.name: i.value for i in EnumKeyType}
        suggestion = None
        result = {}
        try:
            for k, v in dmap.items():
                if isinstance(k, EnumKeyType):
                    result[k] = v
                elif isinstance(k, int):
                    if k in domain.values():
                        result[EnumKeyType(k)] = v
                    else:
                        result[k] = v
                elif isinstance(k, str):
                    if k in domain:
                        result[EnumKeyType[k]] = v
                    else:
                        for dk in domain.keys():
                            if SequenceMatcher(None, dk, k).ratio() >= 0.7:
                                suggestion = dk
                        raise
            return result
        except:
            raise InvalidValueException(
                field_name=info.field_name,
                expected_values=list(domain.keys()),
                FieldType=EnumKeyType,
                actual=k,
                suggestion=suggestion,
            )

    def serialize(
        self, items: dict[(Enum | int), int], info: SerializationInfo
    ) -> dict[(str | int), int]:
        result = {}
        for k, v in items.items():
            if isinstance(k, int):
                result[k] = v
            else:
                result[k.name] = v
        return result
