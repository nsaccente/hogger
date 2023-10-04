from difflib import SequenceMatcher
from enum import Enum, IntFlag
from typing import Any, get_args, get_type_hints, Union

from pydantic import FieldSerializationInfo, FieldValidationInfo, SerializationInfo

from .errors import InvalidValueException


def _get_all_subclasses(cls) -> list[type]:
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(_get_all_subclasses(subclass))
    return subclasses


def pydantic_annotation(cls) -> type:
    subclasses = _get_all_subclasses(cls)
    FinalType = Union[subclasses[0], subclasses[1]]
    for subclass in subclasses[2:]:
        FinalType = Union[FinalType, subclass]
    return FinalType


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
