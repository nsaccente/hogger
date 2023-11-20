import subprocess

import pytest


@pytest.fixture(autouse=True, scope="session")
def my_fixture():
    # setup_stuff
    print(subprocess.run("docker-compose up -d".split()))
    yield
    print(subprocess.run("docker-compose down".split()))

    # teardown_stuff
