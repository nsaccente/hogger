from hogger.engine import WorldTable
from tests.conftest import wt
from time import sleep
import mysql
import pytest


def test_thing(
    # wt: WorldTable
):

    cnx = mysql.connector.connect(
        host="172.18.0.116",
        port="53308",
        database="world_table",
        user="root",
        password="",
        auth_plugin='mysql_native_password',
    )
    if not cnx.is_connected():
        raise Exception(f"Unable to connect to worldserver database")
    

    # wt = WorldTable(
    #     host="172.18.0.116",
    #     port="53308",
    #     database="world_table",
    #     user="root",
    #     password="",
    # )
    # print(f"LOCKED: {wt.is_locked()}")
    # print(wt)

    # # Initialize the hoggerstate table if one doesn't already exist.
    # with self._cnx.cursor() as cursor:
    #     cursor.execute(
    #         """
    #         CREATE TABLE IF NOT EXISTS hoggerstate (
    #             entity_code INT NOT NULL,
    #             hogger_identifier VARCHAR(128) NOT NULL,
    #             db_key INT NOT NULL,
    #             PRIMARY KEY (entity_code, hogger_identifier)
    #         );
    #         """,
    #     )
    #     cursor.execute(
    #         f"""
    #         SELECT *
    #         FROM information_schema.tables
    #         WHERE table_schema = '{self.database}'
    #             AND table_name = 'hoggerlock'
    #         LIMIT 1;
    #         """,
    #     )
    #     exists = len(cursor.fetchall()) > 0
    #     if not exists:
    #         cursor.execute(
    #             """
    #             CREATE TABLE IF NOT EXISTS hoggerlock (
    #                 k VARCHAR(32) NOT NULL,
    #                 v BIT NOT NULL,
    #                 PRIMARY KEY (k)
    #             );
    #             """,
    #         )
    #         cursor.execute(
    #             """
    #             INSERT INTO hoggerlock(k, v) values ("locked", 0);
    #             """,
    #         )