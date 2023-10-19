import os
from hogger.entities import Entity, EntityCodes
from hogger.engine import Manifest


class State(dict[int, dict[str, Entity]]):
    def __init__(self):
        super().__init__({
            entity_code: {} for entity_code, _ in EntityCodes.items()
        })


    @staticmethod
    def _get_manifest_paths(dir_or_file: str) -> list[str]:
        hoggerfiles = []
        if os.path.isfile(dir_or_file):
            hoggerfiles.append(os.path.abspath(dir_or_file))
        elif os.path.isdir(dir_or_file):
            for root, dirs, files in os.walk(".", topdown=False):
                for name in files:
                    if name.endswith(".hogger"):
                        hoggerfiles.append(os.path.abspath(os.path.join(root, name)))
        else:
            raise Exception(
                "Path provided is neither a dir, nor a file."
            )
        return hoggerfiles


    @staticmethod
    def get_desired_state(dir_or_file: str) -> "State":
        desired = State()
        for hoggerfile in State._get_manifest_paths(dir_or_file):
            manifest = Manifest.from_file(hoggerfile)
            entities: list[Entity] = manifest.entities
            for entity in entities:
                entity_code = EntityCodes(type(entity))
                hogger_identifier = entity.hogger_identifier()
                desired[entity_code][hogger_identifier] = entity
        return desired

    
    @staticmethod
    def diff_state(
        desired_state: "State", 
        actual_state: "State",
    ) -> dict[str, "State"]:
        created = State()
        modified = State()
        for entity_code in EntityCodes:
            for hogger_id, des_entity in desired_state[entity_code].items():
                # If hogger_id from desired state exists in actual state,
                # compute the diff; otherwise, add to `created`.
                if hogger_id in actual_state[entity_code]:
                    # If the diff returned has contents in it, add to
                    # `modified`. Otherwise, no action necessary.
                    entity_diff = des_entity.diff(
                        actual_state[entity_code][hogger_id],
                    )
                    if len(entity_diff) > 0:
                        modified[entity_code][hogger_id]
                    del desired_state[entity_code][hogger_id]
                else:
                    created[entity_code][hogger_id] = des_entity
        # Anything remaining in `actual_state` dict will be deleted.
        return (created, modified, actual_state)