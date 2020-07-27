### Overview
Dell EMC OpenManage Ansible Modules unit test scripts are located under
 [unit](./tests/unit) directory.

### Implementing the unit tests
Any contribution must have an associated unit test. This section covers the
 tests that need to be carried out. 
* The unit tests are required for each new resource, bug fix, or enhancement. They must cover what is being submitted.
* The name of the test modules should start with the prefix "test_" in
 addition to the tested module name. For example: test_ome_user

### Prerequisites
* Dell EMC OpenManage collections - to install run `ansible-galaxy collection
 install dellemc.openmanage`
* To run the unittest for iDRAC modules, install OpenManage Python Software Development Kit (OMSDK) using
`pip install omsdk --upgrade` or from [Dell EMC OpenManage Python SDK](https://github.com/dell/omsdk)

### Executing unit tests
You can execute them manually by using any tool of your choice, like `pytest` or `ansible-test`.

#### Executing with `ansible-test`
* Clone [Ansible repository](https://github.com/ansible/ansible) from GitHub to local $ANSIBLE_DIR.
* Copy `compat` directory from the cloned repository path.
 `$ANSIBLE_DIR/test/units/` to the location of the installed Dell EMC OpenManage collection `$ANSIBLE_COLLECTIONS_PATHS/ansible_collections/dellemc/openmanage/tests/unit`.
* Copy `utils.py` file from `$ANSIBLE_DIR/test/units/modules` tests location to the location of the installed collection `$ANSIBLE_COLLECTIONS_PATHS/ansible_collections/dellemc/openmanage/tests/unit/plugins/modules`
* Edit the copied `utils.py` to refer the above `compat` package as below:
```python
      from units.compat import unittest
      from units.compat.mock import patch
       
       # Replace the above lines in utils.py as below
      
      from ansible_collections.dellemc.openmanage.tests.unit.compat import unittest
      from ansible_collections.dellemc.openmanage.tests.unit.compat.mock import patch
```
* To install `ansible-test` requirements use 
    ```
    ansible-test units --requirements
    ```
* To perform a test, run the following command
    ```
    ansible-test units -vvv
    ```
* To run any specific module use the below command,
    ```
    ansible-test units idrac_server_config_profile
    ```
See [here](https://docs.ansible.com/ansible/latest/dev_guide/testing_units.html#testing-units) for more details on unit-testing.

#### Executing with `pytest`

See [here](https://docs.pytest.org/en/stable/).

### Acceptance criteria
The code coverage of new module should be more than 90%.
Execute code coverage with `pytest` as explained [here](https://pytest-cov.readthedocs.io/en/latest/reporting.html).