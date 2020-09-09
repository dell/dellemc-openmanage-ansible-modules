# Build a Docker image of Dell EMC OpenManage Ansible Modules
Build a docker image for Dell EMC OpenManage Ansible Modules by using the Docker Engine and the docker file for OpenManage Ansible Modules. Download the docker file from [here](./Dockerfile).

OpenManage Ansible Modules docker file contains [Ansible](https://pypi.org/project/ansible/), [OpenManage Python SDK (OMSDK)](https://pypi.org/project/omsdk/), and [Python:3-slim](https://hub.docker.com/_/python) image source packages. Ensure that you adhere to the licensing terms and conditions of these packages and get the required approval before building the docker image from this file.

For more information about the Docker Engine and how to install the Docker Engine, see https://docs.docker.com/engine/.


## How to build the Docker image
To build the docker image, do the following:
1. Download and install Docker Engine in your system.
1. Download and save the OpenManage Ansible modules docker file from [here](./Dockerfile). Ensure that this docker file is downloaded on the same system where the docker engine is installed.
1. Run the following Command:
    ```bash
    docker build -t dellemc/openmanage-ansible-modules .
    ```

    An  image with the name _dellemc/openmanage-ansible-modules_ is created. The size of this image will be around 379MB.

    Note:
    * Run the command from the same directory where the Dockerfile is downloaded. If not use the option `--file` to specify the path to Dockerfile.
    * The OpenManage Enterprise docker file uses the official docker image [python:3-slim](https://hub.docker.com/_/python) as a base.
    * Ensure that the `docker.io` registry search path is enabled on the system if the Docker engine fails to download the base image.

1. To verify if the image is created successfully, run the following command:

    ```bash
    docker image ls
    ```

    If the image is created successfully, this command lists the image named as _dellemc/openmanage-ansible-modules_.

## Add playbook, variable files and inventory
The Docker image of OpenManage Ansible Modules does not contain the playbook and the required configuration to run a task.

The latest sample playbooks and examples are available in the [playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/devel/playbooks) directory.

Bind mount the folder containing the playbook, variable and inventory files to the target mount point `/dellemc` using the option `-v`.

### Running a playbook
Run the playbook using the following command after the playbook, inventory and optional variable files are added to the current working directory.

```bash
docker run --rm \
    -v $(pwd):/dellemc dellemc/openmanage-ansible-modules:latest \
    -v playbook.yml -i inventory -t getlcstatus
```

Note:
* To allow access to mounted shares in the docker container, use the volume or bind mount option when running export or import server configuration profile tasks.

### Running ad-hoc commands
Ansible ad-hoc commands can also be used. Following is an example of how to use an ad-hoc command to get the status of a lifecycle controller.

```bash
docker run --rm \
    --entrypoint '/usr/local/bin/ansible' \
    dellemc/openmanage-ansible-modules:latest localhost \
    -m idrac_lifecycle_controller_status_info -a "idrac_ip=192.168.10.1 idrac_user=user idrac_pwd=password"
```
