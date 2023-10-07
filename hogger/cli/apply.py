import mysql.connector

from hogger import Manifest
from hogger.misc import Lookup
from hogger.sql import WorldTable




    
def apply(
    host: str,
    port: (int | str),
    user: str,
    password: str,
    world: str,
    dir_or_file: str,
    **kwargs,
) -> None:
    wt = WorldTable(
        host=host,
        port=port,
        user=user,
        password=password,
        database=world,

    )
    wt.write_test(0, 17, "Martin Fury")
    wt.write_test(0, 25, "Worn Shortsword")
    wt.write_test(0, 35, "Bent Staff")
    wt.get_hoggerstate()



    # entities = []
    # for file in dir_or_file:
    #     print(file)
    #     manifest = Manifest.from_file(file)
    #     entities.extend(manifest.entities)
    
    # for entity in entities:
    #     pass
        # create hoggerstate table if not exists
        # if in hoggerstate table but not in entities, entity must be deleted.
        # if in entities but not in hoggerstate, entity must be created.
        # display this diff to the user; seek confirmation from user.

    # We're going to have to settle on a primary identifier for entities. This
    # is going to be different for each entity type. We can still dynamically
    # allocate entry ids in the database, but refer to entities in hogger files
    # strictly by their primary identifier.
