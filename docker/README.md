# Building a Docker image of Dell EMC OpenManage Ansible Modules
Build a docker image for Dell EMC OpenManage Ansible Modules by using the Docker Engine and the docker file for OpenManage Ansible Modules. Download the OpenManage Ansible Modules docker file from [here](./Dockerfile).

The docker file for OpenManage Ansible Modules contains the following packages:
* [Ansible](https://pypi.org/project/ansible/)
* [OpenManage Python SDK (OMSDK)](https://pypi.org/project/omsdk/)
* [Python:3-slim](https://hub.docker.com/_/python)

Ensure that you adhere to the licensing terms and conditions of the respective packages.

For more information about the Docker Engine and how to install the Docker Engine, see https://docs.docker.com/engine/.


## How to build the Docker image
To build the docker image, do the following:
1. Download and install Docker Engine on your system.
1. Download and save the OpenManage Ansible modules docker file from [here](./Dockerfile). Ensure that this docker file is downloaded on the same system where the Docker Engine is installed.
1. Run the following Command:
    ```bash
    docker build -t dellemc/openmanage-ansible-modules .
    ```

    A docker image is created with the name specified in the command. That is, _dellemc/openmanage-ansible-modules_. The size of this image is around 379 MB.

    Note:
    * Run the command from the same directory where the Dockerfile is downloaded. If not use the option `--file` to specify the path to the Dockerfile.
    * The OpenManage Enterprise docker file uses the official docker image [python:3-slim](https://hub.docker.com/_/python) as a base.
    * Ensure that the `docker.io` registry search path is enabled on the system if the Docker Engine fails to download the base image.

1. To verify if the image is created successfully, run the following command:

    ```bash
    docker image ls
    ```

    If the image is created successfully, this command lists the image created in step 3. That is, _dellemc/openmanage-ansible-modules_.

## Add playbook, variable files and inventory
The Docker image of OpenManage Ansible Modules does not contain the playbook and the required configuration to run a task.

The latest sample playbooks and examples are available in the [playbooks](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/devel/playbooks) directory.

After creating the playbook, bind mount the folder containing the playbook, variable and inventory files to the target mount point `/dellemc` using the option `-v`.

### Running a playbook
Run the playbook using the following command after the playbook, inventory and optional variable files are added to the current working directory.

```bash
docker run --rm \
    -v $(pwd):/dellemc dellemc/openmanage-ansible-modules:latest \
    -v playbook.yml -i inventory -t getlcstatus
```

Note:
* To allow access to mounted shares in the Docker container, use the volume or bind mount option when running export or import server configuration profile tasks.
* If Security-Enhanced Linux (SELinux) is configured on the system, playbook may fail to run. Refer Docker documentation on how to bind mount folders using SELinux label. 

### Running ad-hoc commands
Ansible ad-hoc commands can also be used. The following example command shows how to to view the status of a Lifecycle Controller.

```bash
docker run --rm \
    --entrypoint '/usr/local/bin/ansible' \
    dellemc/openmanage-ansible-modules:latest localhost \
    -m idrac_lifecycle_controller_status_info -a "idrac_ip=192.168.10.1 idrac_user=user idrac_pwd=password"
```
