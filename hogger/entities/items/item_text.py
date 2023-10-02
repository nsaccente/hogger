from pydantic import BaseModel, Field
from enum import Enum
from inspect import cleandoc
from hogger.misc import LookupID


class PageMaterial(Enum):
    Parchment = 1
    Stone = 2
    Marble = 3
    Silver = 4
    Bronze = 5
    Valentine = 6
    Illidan = 7


class Language(Enum):
    Universal = 0
    Orcish = 1
    Darnassian = 2
    Taurahe = 3
    Dwarvish = 6
    Common = 7
    Demonic = 8
    Titan = 9
    Thalassian = 10
    Draconic = 11
    Kalimag = 12
    Gnomish = 13
    Troll = 14
    Gutterspeak = 33
    Draenei = 35
    Zombie = 36
    GnomishBinary = 37
    GoblinBinary = 38


class ItemText(BaseModel):
    pageText: LookupID = Field(
        default=0,
        description=cleandoc(
            """
            The ID of the row in the `page_text` table corresponding to the text
            that will be shown to the player.
            """
        ),
        ge=0,
    )
    pageMaterial: PageMaterial = Field(
        default=PageMaterial.Parchment,
        description=cleandoc(
            """
            The material that the text will be displayed on to the player.
            Defaults to parchment.
            """
        ),
    )
    language: (Language | LookupID) = Field(
        default=Language.Universal,
        description=cleandoc(
            """
            The RPG language that the document will be written in, requiring
            players to be fluent in the document's language in order to read
            it correctly. Defaults to Universal, meaning all players will be
            able to interpret it, with no language requirements.
            """
        ),
    )