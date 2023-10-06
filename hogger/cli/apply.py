import json

import mysql.connector
import yaml
import glob

from hogger import Manifest
from hogger.misc import Lookup


def apply(
    host: str,
    port: (int | str),
    database: str,
    user: str,
    password: str,
    **kwargs,
) -> None:
    # Connect to the worldserver database 
    connection = mysql.connector.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )

    if not connection.is_connected():
        raise Exception("Unable to connect to worldserver database.")

    cursor = connection.cursor()
    # We need the following fields:
    # entity_type, entity_name, entry_in_table, date_created
    f = cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS hoggerstate (
            type VARCHAR(32) NOT NULL,
            name VARCHAR(128) NOT NULL,
            entry INT NOT NULL
        );
        """
    )

    entities = []
    for file in glob.glob(kwargs["glob"]):
        manifest = Manifest.from_file(file)
        entities.extend(manifest.entities)
    
    for entity in entities:
        pass
        # create hoggerstate table if not exists
        # if in hoggerstate table but not in entities, entity must be deleted.
        # if in entities but not in hoggerstate, entity must be created.
        # display this diff to the user; seek confirmation from user.

    # We're going to have to settle on a primary identifier for entities. This
    # is going to be different for each entity type. We can still dynamically
    # allocate entry ids in the database, but refer to entities in hogger files
    # strictly by their primary identifier.
