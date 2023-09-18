import yaml
from pydantic import Field, BaseModel
from typing_extensions import Annotated
from typing import Literal, Union
import abc

from pydantic import BaseModel


class Entity(BaseModel, abc.ABC):
    pass


class Item(Entity, BaseModel, abc.ABC):
    pass


class Weapon(Item, BaseModel, abc.ABC):
    pass


class OneHandedAxe(BaseModel):
    type: Literal['OneHandedAxe']
    name: str


class TwoHandedAxe(BaseModel):
    type: Literal['TwoHandedAxe']
    name: str

class Manifest(BaseModel):
    apiVersion: str = Field(
        description="API version to use against the configuration file.",
    )
    entities: list[Annotated[Union[OneHandedAxe, TwoHandedAxe], Field(discriminator="type")]] 

    @staticmethod
    def from_file(filepath: str) -> "Manifest":
        with open(filepath, 'r') as yaml_file:
            return Manifest(**yaml.safe_load(yaml_file))
        