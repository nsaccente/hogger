from textwrap import dedent
from enum import auto, IntFlag, Enum
from pydantic import BaseModel, Field
from hogger.util import (
    LookupID,
)


class AllowableClass(IntFlag):
    Warrior: int = auto()
    Paladin: int = auto()
    Hunter: int = auto()
    Rogue: int = auto()
    Priest: int = auto()
    DeathKnight: int = auto()
    Shaman: int = auto()
    Mage: int = auto()
    Warlock: int = auto()
    UNUSED: int = auto()
    Druid: int = auto()


class AllowableRace(IntFlag):
    Human: int = auto()
    Orc: int = auto()
    Dwarf: int = auto()
    NightElf: int = auto()
    Undead: int = auto()
    Tauren: int = auto()
    Gnome: int = auto()
    Troll: int = auto()
    Goblin: int = auto()
    BloodElf: int = auto()
    Draenei: int = auto()


class RequiredHonorRank(Enum):
    Undefined = 0
    Private_Scout = 1
    Corporal_Grunt = 2
    Sergeant_Sergeant = 3
    MasterSergeant_SeniorSergeant = 4
    SergeantMajor_FirstSergeant = 5
    Knight_StoneGuard = 6
    KnightLieutenant_BloodGuard = 7
    KnightCaptain_Legionnare = 8
    KnightChampion_Centurion = 9
    LieutenantCommander_Champion = 10
    Commander_LieutenantGeneral = 11
    Marshal_General = 12
    FieldMarshal_Warlord = 13
    GrandMarshal_HighWarlord = 14


class ReputationRank(Enum):
    Hated = 0
    Hostile = 1
    Unfriendly = 2
    Neutral = 3
    Friendly = 4
    Honored = 5
    Revered = 6
    Exalted = 7


class Requires(BaseModel):
    classes: list[AllowableClass | int] = Field(
        default=[],
        description=dedent(
            """
            Classes permitted to use the item.
            """
        ),
    )
    races: list[AllowableRace | int] = Field(
        default=[],
        description=dedent(
            """
            Races permitted to use the item.
            """
        ),
    )
    level: int = Field(
        default=1,
        descrption=dedent(
            """
            The minimum player level required to equip the item.
            """
        ),
        ge=1,
    )
    skill: LookupID = Field(
        default=0,
        description=dedent(
            """
            The skill required to use this item.
            """
        ),
        ge=0,
    )
    skillRank: int = Field(
        default=0,
        description=dedent(
            """
            The required skill rank the player needs to have to use this item.
            """
        ),
    )
    spell: LookupID = Field(
        default=0,
        description=dedent(
            """
            The required spell that the player needs to have to use this item.
            """
        ),
    )
    honorRank: (RequiredHonorRank | int) = Field(
        default=RequiredHonorRank.Undefined,
        description=dedent(
            """
            The required PvP rank required to use the item.",
            serialization_alias="requiredhonorrank",
            """
        ),
    )
    cityRank: int = Field(
        default=0,
        description=dedent(
            """
            Unused. All items have this set to 0.
            """
        ),
        ge=0,
    )
    reputationFaction: int = Field(
        default=0,
        description=dedent(
            """
            The faction template ID of the faction that the player has to have
            a certain ranking with. If this value is 0, the faction of the
            seller of the item is used.
            """
        ),
        ge=0,
    )
    reputationRank: (ReputationRank | int) = Field(
        default=0,
        description=dedent(
            """
            The required reputation rank to use the item.
            """
        ),
    )
    disenchantSkill: int = Field(
        default=0,
        description=dedent(
            """
            The required skill proficiency in disenchanting that the player must
            have in order to disenchant this item.
            """
        ),
        ge=0,
    )
    map: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the map in which this item can be used. If you leave the
            map, the item will be deleted from the inventory.
            """
        ),
        ge=0,
    )
    area: LookupID = Field(
        default=0,
        description=dedent(
            """
            The ID of the zone in which this item can be used. If you leave the
            area, the item will be deleted from the inventory.
            """
        ),
    )
    holiday: LookupID = Field(
        default=0,
        description=dedent(
            """
            The holiday event that must be active in order to use the item.
            """
        ),
    )


    @staticmethod
    def from_sql(
        sql_data: dict[str, any],
        sql_to_model: dict[str, str]={
            "classes": "AllowableClass",
            "races": "AllowableRace",
            "level": "RequiredLevel",
            "skill": "RequiredSkill",
            "skillRank": "RequiredSkillRank",
            "spell": "requiredspell",
            "honorRank": "requiredhonorrank",
            "cityRank": "RequiredCityRank",
            "reputationFaction": "RequiredReputationFaction",
            "reputationRank": "RequiredReputationRank",
            "disenchantSkill": "RequiredDisenchantSkill",
            "map": "Map",
            "area": "area",
            "holiday": "HolidayId",
        },
    ) -> "Requires":
        params = {}
        for sql_field, model_field in sql_to_model.items():
            params[model_field] = sql_data[sql_field] 
        return Requires(*params)