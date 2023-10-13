from inspect import cleandoc
from pydantic import BaseModel, Field
from hogger.util import LookupID


class RandomStat(BaseModel):
    id: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            Points to an entry in item_enchantment_template and ties an iteem's
            chance at having a random property attached to it when it shows up
            for the first time.
            """
        ),
        ge=0,
    )
    withSuffix: bool = Field(
        default=False,
        description=cleandoc(
            """
            Determines whether there will be a random suffix attached to the
            item name. Defaults to False.
            """
        ),
    )

    @staticmethod
    def from_sql(
        RandomProperty: str="RandomProperty",
        RandomSuffix: str="RandomSuffix",
    ):
        def from_sql(sql: dict[str, any]):
            random_property = sql[RandomProperty]
            random_suffix = sql[RandomSuffix]
            with_prefix = (random_suffix != 0)


            if min(random_property, random_suffix) != 0:
                pass
                # raise Exception("Unable to create ")
            return RandomStat(
                id=abs(max(random_property, random_suffix)),
                withPrefix=with_prefix,
            )
        return from_sql
        