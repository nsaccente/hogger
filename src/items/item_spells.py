from enum import Enum
from pydantic import (BaseModel, Field, model_validator)

from src.misc.currency import LookupID


class SpellTrigger(Enum):
    Use: int = 0
    OnEquip: int = 1
    ChanceOnHit: int = 2
    Soulstone: int = 4
    OnUse: int = 5
    LearnSpell: int = 6
    

class ItemSpell(BaseModel):
    id: LookupID 
    trigger: SpellTrigger
    charges: int
    procsPerMinute: int
    # cooldown: Duration
