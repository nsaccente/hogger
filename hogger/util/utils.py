from typing import Union
import os

from mysql.connector.cursor_cext import CMySQLCursor as Cursor


def get_hoggerpaths(dir_or_file: str):
    hoggerfiles = []
    if os.path.isfile(dir_or_file):
        hoggerfiles.append(os.path.abspath(dir_or_file))
    elif os.path.isdir(dir_or_file):
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if name.endswith(".hogger"):
                    hoggerfiles.append(os.path.abspath(os.path.join(root, name)))
    else:
        raise Exception(
            "Path provided is neither a dir, nor a file."
        )
    return hoggerfiles


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


def direct_map(sql_field: str):
    def direct_map(
        sql_dict: dict[str, any],
        cursor: Cursor = None,
        field_type: type = None,
    ) -> any:
        return sql_dict[sql_field]

    return direct_map
