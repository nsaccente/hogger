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


def from_sql(sql_field: str):
    def from_sql(
        sql_dict: dict[str, any],
        cursor: Cursor = None,
        field_type: type = None,
    ) -> any:
        return sql_dict[sql_field]
    return from_sql


def to_sql(sql_field: str):
    def to_sql(
        model_field: str,
        model_dict: dict[str, any],
        cursor: Cursor = None,
        field_type: type = None,
    ) -> dict[str, str]:
        return {sql_field: model_dict[model_field]}
    return to_sql