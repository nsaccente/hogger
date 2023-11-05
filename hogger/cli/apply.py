from contextlib import ExitStack
from functools import partial

from hogger.engine import Manifest, WorldTable, get_hoggerfiles
from hogger.entities import EntityCodes

# wt._write_hoggerstate(1, "Martin Fury", 17)
# wt._write_hoggerstate(1, "Worn Shortsword", 25)
# wt._write_hoggerstate(1, "Bent Staff", 35)
# wt._write_hoggerstate(1, "Spellfire Belt#asdf", 21846)


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
        print("Hogger is locked.")
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

        pending = wt.stage()
        print(pending)

        # response = input("\nApply these changes? (yes/no) ")
        response = "yes"
        if response == "yes":
            wt.apply()
        else:
            print("Exiting")
