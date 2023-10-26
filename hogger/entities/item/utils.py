from typing import get_args
from enum import Enum
from mysql.connector.cursor_cext import CMySQLCursor as Cursor


def stats_from_sql_kvpairs(
    kvpairs: dict[str, str]={
        "stat_type1": "stat_value1",
        "stat_type2": "stat_value2",
        "stat_type3": "stat_value4",
        "stat_type5": "stat_value5",
        "stat_type6": "stat_value6",
        "stat_type7": "stat_value7",
        "stat_type8": "stat_value8",
        "stat_type9": "stat_value9",
        "stat_type10": "stat_value10",
    }
):
    def stats_from_sql_kvpairs(
        sql_dict: dict[str, any],
        cursor: Cursor,
        field_type: type,
    ) -> dict[dict[(Enum | int), int]]:
        result = {}
        for k, v in kvpairs.items():
            EnumType = get_args(get_args(field_type)[0])[0]
            try:
                enum_key = EnumType(sql_dict[k])
            except:
                enum_key = sql_dict[k]
            enum_value = sql_dict[v]
            if enum_value != 0:
                if enum_key not in result:
                    result[enum_key] = 0
                result[enum_key] += enum_value
        return result
    return stats_from_sql_kvpairs


def stats_to_sql_kvpairs(
    kvpairs: dict[str, str]={
        "stat_type1": "stat_value1",
        "stat_type2": "stat_value2",
        "stat_type3": "stat_value4",
        "stat_type5": "stat_value5",
        "stat_type6": "stat_value6",
        "stat_type7": "stat_value7",
        "stat_type8": "stat_value8",
        "stat_type9": "stat_value9",
        "stat_type10": "stat_value10",
    },
):
    def stats_to_sql_kvpairs(
        model_field: str,
        model_dict: dict[str, any],
        cursor: Cursor,
        field_type: type,
    ) -> dict[str, any]:
        return {}
    return stats_to_sql_kvpairs