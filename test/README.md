### Overview
Dell EMC OpenManage Ansible Modules unit test scripts are located under [units](units) folder.

### Implementing the unit tests
Any contribution must have an associated unit test.This section covers the tests that need to be carried out. 
* The unit tests are required for each new resource, bug fix, or enhancement. They must cover what is being submitted.
* The name of the test modules should start with the prefix "test_" in addition to the tested module name. For example- test_ome_user

### Executing unit tests
You can execute them manually by using any tool of your choice, like `pytest` or `ansible-test`.

##### Executing with `ansible-test`

See [here](https://docs.ansible.com/ansible/latest/dev_guide/testing_units.html#testing-units).

##### Executing with `pytest`

See [here](https://docs.pytest.org/en/2.8.7/usage.html).

### Acceptance criteria
The code coverage of new module should be more than 90%.

Execute code coverage with `pytest` [here](https://pytest-cov.readthedocs.io/en/latest/reporting.html).