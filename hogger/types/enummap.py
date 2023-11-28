from difflib import SequenceMatcher
from enum import Enum
from typing import get_args, get_type_hints

from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import SerializationInfo

from hogger.types import EnumUtils
from hogger.util import InvalidValueException


class EnumMapUtils:
    @staticmethod
    def parse(
        cls,
        dmap: dict[(str | int), int],
        info: SerializationInfo,
    ) -> dict[(Enum | int), int]:
        EnumKeyType = (
            list(
                filter(
                    lambda field_type: (issubclass(field_type, Enum)),
                    get_args(get_args(get_type_hints(cls)[info.field_name])[0]),
                ),
            )
        )[0]

        domain = {i.name: i.value for i in EnumKeyType}
        suggestion = None
        result = {}
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
                    raise InvalidValueException(
                        field_name=info.field_name,
                        expected_values=list(domain.keys()),
                        FieldType=EnumKeyType,
                        actual=k,
                        suggestion=suggestion,
                    )
        return result

    def serialize(
        self,
        items: dict[(Enum | int), int],
        info: SerializationInfo,
    ) -> dict[(str | int), int]:
        result = {}
        for k, v in items.items():
            if isinstance(k, int):
                result[k] = v
            else:
                result[k.name] = v
        return result

    @staticmethod
    def from_sql_named_fields(field_map: dict[str, str]):
        """
        Use when the sql table has items typically stored in an enummap are
        defined in their own column, e.g. fire_res, frost_res, etc.

        The key should be the field in the sql table, and the value should map
        to the name for the enum it's mapped to.
        """

        def from_sql_named_fields(
            sql_dict: dict[str, any],
            hogger_identifier: str,
            cursor: Cursor,
            field_type: type,
        ) -> dict[dict[(Enum | int), int]]:
            EnumType = get_args(get_args(field_type)[0])[0]
            result = {}
            for sql_field, model_field in field_map.items():
                if sql_dict[sql_field] != 0:
                    EnumUtils.resolve(model_field, EnumType)
                    result[model_field] = sql_dict[sql_field]
            return result

        return from_sql_named_fields

    @staticmethod
    def to_sql_named_fields(field_map: dict[str, str]):
        def to_sql_named_fields(
            model_field: str,
            model_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> dict[str, any]:
            d = {value: 0 for value in field_map.values()}
            for k, v in model_dict[model_field].items():
                d[field_map[k.name]] = v
            return d

        return to_sql_named_fields
