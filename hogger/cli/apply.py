from contextlib import ExitStack
from functools import partial

from hogger.engine import Manifest, WorldTable, get_hoggerfiles
from hogger.entities import EntityCodes


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

        # Load manifests and add them to the WorldTable object's desired state.
        for hoggerfile in get_hoggerfiles(dir_or_file):
            manifest = Manifest.from_file(hoggerfile)
            wt.add_desired(*manifest.entities)
        
        wt.stage()

        print("\nTo Be Created:")
        for entity_code in wt._created:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in wt._created[entity_code]:
                print(f"  {entity_type}.{hogger_id}")

        print("\nTo Be Modified:")
        for entity_code in wt._modified:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in wt._modified[entity_code]:
                print(f"  {entity_type}.{hogger_id}")

        print("\nUnchanged:")
        for entity_code in wt._unchanged:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in wt._unchanged[entity_code]:
                print(f"  {entity_type}.{hogger_id}")

        print("\nTo Be Deleted:")
        for entity_code in wt._deleted:
            entity_type = EntityCodes[entity_code].__name__
            for hogger_id in wt._deleted[entity_code]:
                print(f"  {entity_type}.{hogger_id}")

        # response = input("\nApply these changes? (yes/no) ")
        # response = "yes"
        # if response == "yes":
        #     wt.apply(
        #         to_be_created=created,
        #         to_be_modified=modified,
        #         to_be_deleted=deleted,
        #     )
        # else:
        #     print("Exiting")
