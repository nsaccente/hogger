import docker
from docker.models.containers import Container
from docker.models.volumes import Volume
from docker.types import Mount
import subprocess
from contextlib import ExitStack
from hogger.engine import WorldTable
from functools import partial
import pytest


def _world_table(
    image: str,
    database: str,
    host: str,
    port: (str | int),
    user: str,
    password: str,
    root_password: str,
):
    client = docker.from_env()
    if subprocess.run(["docker", "pull", image]).returncode == 1:
        raise Exception(
            f"Unable to pull image '{image}'. Make sure the Docker daemon is "
            "running. If problems persist, you can pull the image manually."
        )
    
    with ExitStack() as stack:
        container: Container = client.containers.run(
            image=image,
            detach=True,
            environment={
                "MYSQL_ROOT_PASSWORD": root_password,
                "MYSQL_USER": user,
                "MYSQL_PASSWORD": password,
                "MYSQL_DATABASE": database,
            },
            name="hogger-test-container",
            ports={f"{port}/tcp": 3306},
        )

        stack.callback(partial(container.remove, v=True))
        stack.callback(container.stop)
        yield WorldTable(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )


_wt: WorldTable = _world_table(
    image = "mariadb:11.1.2",
    database = "world_table",
    host = "localhost",
    port = "3306",
    user = "acore",
    password = "acore",
    root_password = "acore_root",
)

@pytest.fixture
def wt() -> WorldTable:
    return _wt
