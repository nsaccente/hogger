from hogger.manifest import Manifest
from hogger.entities import Entity, EntityCodes
from hogger.sql import WorldTable
from hogger.util import get_hoggerpaths
from contextlib import ExitStack
from functools import partial


def apply(
    host: str,
    port: (int | str),
    user: str,
    password: str,
    world: str,
    dir_or_file: str,
    **kwargs,
) -> None:
    # All of your database interactions through the WorldTable object.
    # Connect to WorldTable before bothering with parsing anything.
    wt = WorldTable(
        host=host,
        port=port,
        user=user,
        password=password,
        database=world,
    )

    # wt._write_hoggerstate(1, "Martin Fury", 17)
    # wt._write_hoggerstate(1, "Worn Shortsword", 25)
    # wt._write_hoggerstate(1, "Bent Staff", 35)
    # wt._write_hoggerstate(1, "Spellfire Belt#asdf", 21846)

    # Confirm unlocked, then Lock hogger.
    if wt.is_locked():
        # TODO: Can't do anything while it's not locked.
        exit(1)

    # Enter an ExitStack to defer releasing hoggerlock.
    with ExitStack() as stack:
        print("Acquiring hoggerlock.")
        wt.acquire_lock()
        stack.callback(wt.release_lock)
        stack.callback(partial(print, "Releasing hoggerlock."))

        # Load all entities 
        desired_states: dict[int, dict[str, Entity]] = {
            entity_code: {} for entity_code, _ in EntityCodes.items()
        }
        for hoggerfile in get_hoggerpaths(dir_or_file):
            manifest = Manifest.from_file(hoggerfile)
            entities: list[Entity] = manifest.entities
            for entity in entities:
                entity_code = EntityCodes(type(entity))
                hogger_identifier = entity.hogger_identifier()
                desired_states[entity_code][hogger_identifier] = entity
        
        # # Load entities from hoggerstate
        hoggerstates = wt.get_hoggerstate()
        actual_states: dict[int, dict[str, Entity]] = {
            entity_code: {} for entity_code, _ in EntityCodes.items()
        }
        for entity_code, hogger_identifier, db_key in hoggerstates:
            actual_states[entity_code][hogger_identifier] = (
                wt.resolve_hoggerstate(
                    entity_code=entity_code, 
                    hogger_identifier=hogger_identifier,
                    db_key=db_key, 
                )
            )

        # Compare actual and desired
        created : dict[int, dict[str, Entity]] = {
            entity_code: {} for entity_code, _ in EntityCodes.items()
        }
        modified: dict[int, dict[str, Entity]] = {
            entity_code: {} for entity_code, _ in EntityCodes.items()
        }
        for entity_code in EntityCodes:
            for hogger_id, des_entity in desired_states[entity_code].items():
                # If hogger_id from desired state exists in actual state,
                # compute the diff; otherwise, add to `created`.
                if hogger_id in actual_states[entity_code]:
                    # If the diff returned has contents in it, add to
                    # `modified`. Otherwise, no action necessary.
                    entity_diff = des_entity.diff(
                        actual_states[entity_code][hogger_id],
                    )
                    if len(entity_diff) > 0:
                        modified[entity_code][hogger_id]
                    del desired_states[entity_code][hogger_id]
                else:
                    created[entity_code][hogger_id] = des_entity
        # Anything remaining in `actual_state` dict will be deleted.
        deleted = actual_states

        
        print()
        print("To Be Created:")
        for c in created[1]:
            print(c)

        print()
        print("To Be Modified:")
        for m in modified[1]:
            print(m)

        print()
        print("To Be Deleted:")
        for d in deleted[1]:
            print(d)

        # Seek confirmation

        # Write

