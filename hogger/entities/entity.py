from abc import ABCMeta, abstractstaticmethod
from inspect import cleandoc
from typing import Any

from pydantic import BaseModel, Field


class Entity(
    BaseModel,
    metaclass=ABCMeta,
):
    type: Any = Field(
        description=cleandoc(
            """
            This field tells the parser which object to use
            """
        ),
    )

    @abstractstaticmethod
    def table_name() -> str:
        """
        Provides invokers with the name of the database that this class governs.
        """
        return "item_template"

    @abstractstaticmethod
    def db_key() -> str:
        """
        Provides invokers with the primary key in the database that uniquely
        identifies instances of this class.
        """
        return "entry"

    @abstractstaticmethod
    def hogger_identifier() -> str:
        """
        Provides invokers with the field within this class that acts as the
        primary identifier for Hogger.
        """
        return "name"