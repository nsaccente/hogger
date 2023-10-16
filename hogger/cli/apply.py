from hogger.manifest import Manifest
from hogger.sql import WorldTable
from hogger.util import get_hoggerpaths
from contextlib import ExitStack
from functools import partial

# wt._write_hoggerstate(0, "Martin Fury", 17)
# wt._write_hoggerstate(0, "Worn Shortsword", 25)
# wt._write_hoggerstate(0, "Bent Staff", 35)
# wt._write_hoggerstate(0, "Spellfire Belt#asdf", 21846)

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

    # Confirm unlocked, then Lock hogger.
    if wt.is_locked():
        # TODO: Can't do anything while it's not locked.
        exit(1)

    # Enter an ExitStack to defer releasing hoggerlock.
    with ExitStack() as stack:
        wt.acquire_lock()
        stack.callback(wt.release_lock)
        stack.callback(partial(print, "Releasing hoggerlock."))

        # Load all entities 
        desired_states = {}
        for hoggerfile in get_hoggerpaths(dir_or_file):
            manifest = Manifest.from_file(hoggerfile)
            entities: list = manifest.entities
            for entity in entities:
                entity_type = entity.entity_type()
                hogger_identifier = entity.hogger_identifier()
                if entity_type not in desired_states:
                    desired_states[entity_type] = {}
                desired_states[entity_type][hogger_identifier] = entity
        

        # Load entities from hoggerstate
        hoggerstates = wt.get_hoggerstate()
        actual_states = {}
        for entity_type, hogger_identifier, db_key in hoggerstates:
            if entity_type not in actual_states:
                actual_states[entity_type] = {} 
            actual_states[entity_type][hogger_identifier] = (
                wt.resolve_hoggerstate(
                    entity_type=entity_type, 
                    hogger_identifier=hogger_identifier,
                    db_key=db_key, 
                )
            )
        
        # for entity_type in actual_states:
        #     for actual_state in actual_states[entity_type]:
                # print(actual_state)

        # Compare actual and desired
        
        # Seek confirmation

        # Write

