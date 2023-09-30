from pydantic import Field, BaseModel

from src.misc.currency import LookupID


class RandomStat(BaseModel):
    id: LookupID = Field(
        default=0,
        description=(
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
        description=(
            """
            Determines whether there will be a random suffix attached to the
            item name. Defaults to False.
            """
        ),
    )
