import mysql.connector
import yaml

from src.manifest import Manifest


def apply(
    host: str,
    port: (int | str),
    database: str,
    user: str,
    password: str,
    **kwargs,
) -> None:
    manifest = Manifest.from_file("./leeroy.yml")
    yml = yaml.dump(manifest.model_dump(by_alias=True), sort_keys=False)
    yml = yaml.dump(vars(manifest), sort_keys=False)
    print(yml)
    # for entity in manifest.entities:
    #     for k, v in entity.model_dump(by_alias=True).items():
    #         print(f"{k}: {v}")
    #     print()

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
