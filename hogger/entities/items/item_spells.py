from enum import Enum
from inspect import cleandoc

from pydantic import BaseModel, Field, model_validator

from hogger.misc import Duration, LookupID


class SpellTrigger(Enum):
    Use: int = 0
    OnEquip: int = 1
    ChanceOnHit: int = 2
    Soulstone: int = 4
    OnUse: int = 5
    LearnSpell: int = 6


class ItemSpell(BaseModel):
    id: LookupID = Field(
        default=-1,
        description=cleandoc(
            """
            The spell ID of the spell that the item can cast or trigger.
            """
        ),
        serialization_alias="spellid_{}",
    )
    trigger: SpellTrigger = Field(
        default=0,
        description=cleandoc(
            """
            The type of trigger for the spell.
            """
        ),
        serialization_alias="spelltrigger_{}",
    )
    charges: int = Field(
        default=0,
        description=cleandoc(
            """
            The number of times that the item can cast the spell. If 0, then
            infinite charges are possible. If negative, then after the number of
            charges is depleted, the item is deleted as well. If positive, then
            the item is not deleted after all the charges are spent.
            """
        ),
        serialization_alias="spellcharges_{}",
    )
    procsPerMinute: int = Field(
        default=0,
        description=cleandoc(
            """
            The proc per minute rate controlling how often the spell is
            triggered. This field is only relevant if `trigger = ChanceOnHit`.
            """
        ),
        serialization_alias="spellppmRate_{}",
    )
    cooldown: Duration = Field(
        default=Duration(),
        description=cleandoc(
            """
            The cooldown in milliseconds for the specific spell controlling how
            often the spell can be used. Use -1 to use the default spell
            cooldown.  Note: this is not the "internal cooldown" of procs
            commonly found on items such as trinkets with "Chance on hit"
            effects.
            """
        ),
        serialization_alias="spellcooldown_{}",
    )
    category: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            The category the spell is in. Default is 0.
            """
        ),
        serialization_alias="spellcategory_{}",
    )
    cooldownCategory: Duration = Field(
        default=-1,
        description=cleandoc(
            """
            The cooldown time that is applied to all other spells in the
            category that the triggered spell is also in. Use -1 to use the
            default spell cooldown. Default is -1.

            Note: `ItemSpell` objects can have both a `cooldown` and a
            `spellCategoryCooldown`, they're not mutually exclusive.
            """
        ),
        serialization_alias="spellcategorycooldown_{}",
    )
