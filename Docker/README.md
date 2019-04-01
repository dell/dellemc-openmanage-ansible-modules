# dellemc-openmanage-ansible-modules
Docker image for [Dell EMC OpenManage Ansible Modules](https://github.com/dell/dellemc-openmanage-ansible-modules)
## Usage
`dellemc-openmanage-ansible-modules` contains no playbook or configuration. One need to pass playbook, var files and inventory for running a task

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
