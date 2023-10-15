import json

import yaml
from pydantic import BaseModel, Field

from hogger.entities import Entity
from hogger.util.utils import pydantic_annotation

Entity = pydantic_annotation(Entity)


class Manifest(BaseModel):
    apiVersion: str = Field(
        description="API version to use against the configuration file.",
    )
    entities: list[Entity]

    @staticmethod
    def from_file(filepath: str) -> "Manifest":
        with open(filepath, "r") as yaml_file:
            return Manifest(**yaml.safe_load(yaml_file))

    def yaml_dump(
        self,
        by_alias: bool = False,
        exclude_unset: bool = True,
    ) -> str:
        return yaml.dump(
            json.loads(
                self.model_dump_json(
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                )
            ),
            indent=2,
            sort_keys=False,
        )
