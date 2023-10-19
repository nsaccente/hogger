from typing import Union


from mysql.connector.cursor_cext import CMySQLCursor as Cursor


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
