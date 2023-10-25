from contextlib import ExitStack
from functools import partial

from hogger.engine import Manifest, State, WorldTable
from hogger.entities import Entity, EntityCodes


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
        stack.callback(partial(print, "\nReleasing hoggerlock."))

        # Compare actual and desired
        created, modified, changes, unchanged, deleted = State.diff_state(
            desired_state=State.get_desired_state(dir_or_file),
            actual_state=wt.get_hoggerstate(),
        )

        # print("\nTo Be Created:")
        # for entity_code in created:
        #     entity_type = EntityCodes[entity_code].__name__
        #     for hogger_id in created[entity_code]:
        #         print(f"  {entity_type}.{hogger_id}")

        # print("\nTo Be Modified:")
        # for entity_code in modified:
        #     entity_type = EntityCodes[entity_code].__name__
        #     for hogger_id in modified[entity_code]:
        #         print(f"  {entity_type}.{hogger_id}")

        # print("\nUnchanged:")
        # for entity_code in unchanged:
        #     entity_type = EntityCodes[entity_code].__name__
        #     for hogger_id in unchanged[entity_code]:
        #         print(f"  {entity_type}.{hogger_id}")

        # print("\nTo Be Deleted:")
        # for entity_code in deleted:
        #     entity_type = EntityCodes[entity_code].__name__
        #     for hogger_id in deleted[entity_code]:
        #         print(f"  {entity_type}.{hogger_id}")

        # response = input("\nApply these changes? (yes/no) ")
        response = "yes"
        if response == "yes":
            pass
            wt.apply(
                to_be_created=created,
                to_be_modified=modified,
                to_be_deleted=deleted,
            )
        else:
            print("Exiting")
