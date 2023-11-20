from hogger.engine import WorldTable


def test_thingy():
    wt = WorldTable(
        host="localhost",
        port="53306",
        database="world_table",
        user="root",
        password="",
    )
    print(wt.is_locked())
