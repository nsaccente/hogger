from inspect import cleandoc

from mysql.connector.cursor_cext import CMySQLCursor as Cursor
from pydantic import BaseModel, Field

from hogger.types import LookupID


class RandomStat(BaseModel):
    id: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            Points to an entry in item_enchantment_template and ties an iteem's
            chance at having a random property attached to it when it shows up
            for the first time.
            """,
        ),
        ge=0,
    )
    withSuffix: bool = Field(
        default=False,
        description=cleandoc(
            """
            Determines whether there will be a random suffix attached to the
            item name. Defaults to False.
            """,
        ),
    )

    @staticmethod
    def from_sql(
        RandomProperty: str = "RandomProperty",
        RandomSuffix: str = "RandomSuffix",
    ):
        def from_sql(
            sql_dict: dict[str, any],
            cursor: Cursor = None,
            field_type: type = None,
        ):
            random_property = sql_dict[RandomProperty]
            random_suffix = sql_dict[RandomSuffix]
            with_prefix = random_suffix != 0
            if min(random_property, random_suffix) != 0:
                pass
                # raise Exception("Unable to create ")
            return RandomStat(
                id=abs(max(random_property, random_suffix)),
                withPrefix=with_prefix,
            )

        return from_sql

    @staticmethod
    def to_sql(
        RandomProperty: str = "RandomProperty",
        RandomSuffix: str = "RandomSuffix",
    ):
        def to_sql(
            model_field: str,
            model_dict: dict[str, any],
            cursor: Cursor,
            field_type: type,
        ) -> dict[str, any]:
            prop, suff = 0, 0
            withSuffix = model_dict[model_field].withSuffix
            prop = model_dict[model_field].id * (not withSuffix)
            suff = model_dict[model_field].id * (withSuffix)
            if prop != 0 and suff != 0:
                # TODO: Create more detailed exception
                raise Exception(
                    f"Both {RandomProperty} and {RandomSuffix} cannot be "
                    "nonzero."
                )
            return {
                RandomProperty: prop,
                RandomSuffix: suff,
            }
        return to_sql
