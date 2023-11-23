from contextlib import ExitStack
from functools import partial

from hogger.engine import Manifest, WorldDatabase, get_hoggerfiles
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
    print(kwargs)
    # All of your database interactions through the WorldTable object.
    # Connect to WorldTable before bothering with parsing anything.
    db = WorldDatabase(
        host=host,
        port=port,
        user=user,
        password=password,
        database=world,
    )

    # Confirm unlocked, then Lock hogger.
    if db.is_locked():
        # TODO: Can't do anything while it's not locked.
        print("Hogger is locked.")
        exit(1)

    # Enter an ExitStack to defer releasing hoggerlock.
    with ExitStack() as stack:
        print("Acquiring hoggerlock.")
        db.acquire_lock()
        stack.callback(db.release_lock)
        stack.callback(partial(print, "\nReleasing hoggerlock."))

        # Load manifests and add them to the WorldTable object's desired state.
        for hoggerfile in get_hoggerfiles(dir_or_file):
            manifest = Manifest.from_file(hoggerfile)
            db.add_desired(*manifest.entities)

        pending = db.stage()
        print(pending)

        # Check for -y/--skip_confirmation
        response = "yes"
        if not kwargs["skip_confirmation"]:
            response = input("\nApply these changes? (yes/no) ")

        if response == "yes":
            print("Applying Hoggerstate changes")
            db.apply()
        else:
            print("Exiting")
