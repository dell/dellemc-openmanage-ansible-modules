# Containerizing Dell EMC OpenManage Ansible Modules
Containerized image of Dell EMC OpenManage Ansible Modules can be built using the dockerfile available [here](./Dockerfile). We will be using Docker Engine for containerizing OpenManage Ansible Modules. More information about Docker Engine and install instructions can be found [here](https://docs.docker.com/engine/).

## Build
Download [Dockerfile](./Dockerfile) to the machine where Docker Engine is installed and run below command. 
```bash
docker build -t dellemc/openmanage-ansible-modules .
```
Upon success, new image with name _dellemc/openmanage-ansible-modules_ will be created. One can verify successful creation of image using command `docker image ls` which will list newly created image with repository name as _dellemc/openmanage-ansible-modules_.

Note: This command need to be run from same directory where Dockerfile is downloaded. If not use the option `--file` to specify the path to Dockerfile.
## Usage
`dellemc/openmanage-ansible-modules` docker image contains no playbook or configuration. One need to pass playbook, var files and inventory for running a task

### Ansible inventory, vars_files and playbooks
Setup a volume or use a bind mount folder containing ansible inventory, vars_files and playbook. This need to be mounted into the container using -v or --mount.

Modules are configured to run with python in `/usr/local/bin/python`. Hence 'ansible_python_interpreter' option need to be set in inventory file or passed as argument while running the playbook with `-e` option

### Running playbook
Once playbook, inventory and variable files are set in the current working directory, one can run the playbook as shown below
```bash
docker run --rm \
    -v $(pwd):/dellemc dellemc/openmanage-ansible-modules:latest \
    -v playbook.yml -i inventory -t getlcstatus \
    -e 'ansible_python_interpreter=/usr/local/bin/python'
```
### Running ad-hoc commands
Ansible ad-hoc commands can also be run with following command.
```bash
docker run --rm \
    --entrypoint '/usr/local/bin/ansible' \
    dellemc/openmanage-ansible-modules:latest localhost \
    -m dellemc_get_lcstatus -a "idrac_ip=192.168.10.1 idrac_user=user idrac_pwd=password"
```
