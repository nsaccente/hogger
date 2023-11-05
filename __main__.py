# from hogger.cli.main import main

# if __name__ == "__main__":
#     main()


# import docker
# from docker.models.containers import Container
# import subprocess
# from contextlib import ExitStack
# from hogger.engine import WorldTable
# from functools import partial


# image = "mariadb:11.1.2"
# database = "world_table"
# host = "localhost"
# port = "3308"
# user = "acore"
# password = "acore"
# root_password = "acore_root"

# client = docker.from_env()
# if subprocess.run(["docker", "pull", image]).returncode == 1:
#     raise Exception(
#         f"Unable to pull image '{image}'. Make sure the Docker daemon is "
#         "running. If problems persist, you can pull the image manually."
#     )

# with ExitStack() as stack:
#     container: Container = client.containers.run(
#         image=image,
#         detach=True,
#         environment={
#             "MYSQL_ROOT_PASSWORD": root_password,
#             "MYSQL_USER": user,
#             "MYSQL_PASSWORD": password,
#             "MYSQL_DATABASE": database,
#         },
#         ports={f"3306/tcp": ("127.0.0.1", 3308)},
#     )

#     stack.callback(partial(container.remove, v=True))
#     stack.callback(container.stop)
    
#     from time import sleep
#     sleep(3*60)

#     print(
#         WorldTable(
#             host=host,
#             port=port,
#             database=database,
#             user=user,
#             password=password,
#         ),
#     )

import subprocess
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from time import sleep
from tqdm import tqdm

IMAGE="mariadb:11.1.2"
if subprocess.run(["docker", "pull", IMAGE]).returncode == 1:
    raise Exception(
        f"Unable to pull image '{IMAGE}'. Make sure the Docker daemon is "
        "running. If problems persist, you can pull the image manually."
    )

container = DockerContainer(image=IMAGE)
container.env={
   "MARIADB_ALLOW_EMPTY_ROOT_PASSWORD": "1",
   "MARIADB_ALLOW_EMPTY_PASSWORD": "1",
}
container.start()
waiting = wait_for_logs(container, "ready for connections")
print(container.get_container_host_ip)
for i in tqdm(range(20)):
   sleep(1)
