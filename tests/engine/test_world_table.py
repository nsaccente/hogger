from hogger.engine import WorldTable
from tests.conftest import wt
from typing import Generator


def test_thing(wt):
    print(wt)
    # from time import sleep
    # sleep(1000)