import json

import mysql.connector
import yaml

from hogger import Manifest, Entity, Item, OneHandedAxe
from hogger.sql.sql_state import SQLState


def apply(
    host: str,
    port: (int | str),
    database: str,
    user: str,
    password: str,
    **kwargs,
) -> None:
    manifest = Manifest.from_file("./leeroy.yml")

    for entity in manifest.entities:
        print(type(entity))

    print(manifest.yaml_dump())

    # connection = mysql.connector.connect(
    #     host=host,
    #     port=port,
    #     database=database,
    #     user=user,
    #     password=password,
    # )
    # if connection.is_connected():
    #     cursor = connection.cursor()

    #     # Define the SQL query to select data from the "acore_world" table
    #     query = "SELECT * FROM creature; "

    #     # Execute the query
    #     cursor.execute(query)

    #     # Fetch all the rows
    #     rows = cursor.fetchall()

    #     # Process and print the results
    #     for row in rows:
    #         print(row)
