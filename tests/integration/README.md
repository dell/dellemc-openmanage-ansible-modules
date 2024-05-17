### Overview
Dell OpenManage Ansible Modules integration test scripts are located under [integration](./) directory.

### Implementing the integration tests
Any contribution must have an associated integration test. This section covers the
 tests that need to be carried out. 
* The integration tests are required for each new resource, bug fix, or enhancement. They must cover what is being submitted.
* The name of the integration test playbooks should be module name and test should be placed under target folder.
* If the test is for something other than modules, like workflow based integration tests, name it accordingly and place it under targets folder.

For example test for module: idrac_session is made available as a directory under targets folder, the folders under target follow kind of role based structure. 

### Prerequisites
* Dell OpenManage collections - to install run `ansible-galaxy collection install dellemc.openmanage`
* Clone the [integration](./) directory to [tests](./tests) directory.

### Executing integration tests with `ansible-test`
* Update `inventory.networking` located at `$ANSIBLE_COLLECTIONS_PATHS/ansible_collections/dellemc/openmanage/tests/integration/`
* Change your working directory to the location of the installed Dell OpenManage collection `$ANSIBLE_COLLECTIONS_PATHS/ansible_collections/dellemc/openmanage/`
* To execute all tests present under targets, run the following command
    ```
    ansible-test network-integration
    ```
* To execute tests for specific target, run the following command
    ```
    ansible-test network-integration "target-name"
    ```
  For example: To execute tests for idrac_session, run the following command
    ```
    ansible-test network-integration idrac_session
    ```

See [here](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html) for more details on integration test capabilities provided by ansible.

### Acceptance criteria
The integration test based code coverage of new module should be 100%.
