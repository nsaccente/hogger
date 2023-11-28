from enum import Enum
from typing import get_args

from mysql.connector.cursor_cext import CMySQLCursor as Cursor

from hogger.entities.item import ItemStat


def stats_from_sql_kvpairs(
    kvpairs: dict[str, str] = {
        "stat_type1": "stat_value1",
        "stat_type2": "stat_value2",
        "stat_type3": "stat_value3",
        "stat_type4": "stat_value4",
        "stat_type5": "stat_value5",
        "stat_type6": "stat_value6",
        "stat_type7": "stat_value7",
        "stat_type8": "stat_value8",
        "stat_type9": "stat_value9",
        "stat_type10": "stat_value10",
    },
):
    def stats_from_sql_kvpairs(
        sql_dict: dict[str, any],
        cursor: Cursor,
        field_type: type,
        hogger_identifier: str,
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
    kvpairs: dict[str, str] = {
        "stat_type1": "stat_value1",
        "stat_type2": "stat_value2",
        "stat_type3": "stat_value3",
        "stat_type4": "stat_value4",
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
        s: tuple[ItemStat, int] = tuple(model_dict[model_field].items())
        res = {}
        i = 0
        for stat_type, stat_value in kvpairs.items():
            if i < len(s):
                res[stat_type] = int(s[i][0])
                res[stat_value] = int(s[i][1])
                i += 1
            else:
                res[stat_type] = 0
                res[stat_value] = 0
        res["StatsCount"] = i
        return res

    return stats_to_sql_kvpairs


def tag_from_sql():
    def tag_from_sql(
        sql_dict: dict[str, any],
        cursor: Cursor,
        field_type: type,
        hogger_identifier: str,
    ) -> dict[str, any]:
        tups = hogger_identifier.rsplit("#", 1)
        if len(tups) == 2:
            return tups[1]
        return ""

    return tag_from_sql
