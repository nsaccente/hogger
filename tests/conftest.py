import subprocess
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from hogger.engine import WorldTable
from time import sleep
import pytest


@pytest.fixture
def wt() -> WorldTable:
    IMAGE = "mariadb:11.1.2"
    DATABASE = "world_table"
    USER = "test"

    # Run the docker pull as a separate process since relying on testcontainers to
    # pull through the API on windows gives me some issue.
    if subprocess.run(["docker", "pull", IMAGE]).returncode == 1:
        raise Exception(
            f"Unable to pull image '{IMAGE}'. Make sure the Docker daemon is "
            "running. If problems persist, you can pull the image manually."
        )

    container = DockerContainer(image=IMAGE)
    container.env={
        "MARIADB_ALLOW_EMPTY_ROOT_PASSWORD": "1",
        "MARIADB_USER": USER,
        "MARIADB_ALLOW_EMPTY_PASSWORD": "1",
        "MARIADB_DATABASE": DATABASE,

    }
    container.with_exposed_ports(3306)
    container.start()
    wait_for_logs(container, "ready for connections")
    # sleep(20000)
    print(
        container
    )
    # yield container
    yield WorldTable(
        host="172.18.0.116",
        # host=container.get_container_host_ip(),
        port=container.get_exposed_port(3306),
        database=DATABASE,
        user=USER,
        password="",
    )
    sleep(10)
    # container.stop()
