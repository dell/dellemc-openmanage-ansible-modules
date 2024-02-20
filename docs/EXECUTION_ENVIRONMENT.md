# Using Ansible Automation Platform with Dell OpenManage Ansible Modules
Creating automation execution environments using the OpenManage Ansible Modules enables your automation teams to define, build, and update their automation environment themselves. Execution environments provide a common language to communicate automation dependency between automation developers, architects, and platform administrators.

In this tutorial, you will learn how to build the execution environment image, push the image to a registry, and then create the execution environment in Ansible Automation Platform.

## Why Ansible Automation Platform over Galaxy

While Ansible Galaxy is good for testing the latest and greatest developer content, it is difficult to find the author who uploaded the content and if the content is supported. Whereas Ansible Automation Platform has bundles of modules, plugins, roles, and documentation from Red Hat. The Ansible Automation Platform provides the following benefits:

- Red Hat Certified content.
- The content can be directly used in your own Ansible playbooks.
- Private Ansible Automation hub can be used within the organization to publish and collaborate.
- Premium support enables you to get help directly from Red Hat if you have any issue with an official Red Hat collection or certified partner collection.
- Red Hat subscription provides free and unlimited access to any content available.


## Workflow
In this tutorial, you will learn how to:
1. [Build execution environment image.](#build-execution-environment-image)
2. [Use Ansible Runner to verify the execution environment (Optional).](#use-ansible-runner-to-verify-the-execution-environment)
3. [Upload the execution environment to a registry.](#upload-the-execution-environment-to-a-registry)
4. [Create execution environment in Ansible Automation Platform.](#create-execution-environment-in-ansible-automation-platform)

## Build execution environment image
Build a image with the required Ansible collections and libraries, and then upload it to a registry of your choice. In this tutorial, you will learn how to create a Podman image.

1. Create the following files in your local directory:
   - *execution-environment.yml*
   - *requirements.yml* 
   - *requirements.txt*
2. For installing OpenManage collections and their dependencies, copy the metadata from the [dellemc.openmanage](https://github.com/dell/dellemc-openmanage-ansible-modules) GitHub repository.

    The following are the sample files:

    **execution-environment.yml**

    ```yaml
    version: 3
    dependencies:
      galaxy: requirements.yml
      python: requirements.txt
      system: bindep.txt
    ```
    
    We can modify the execution environment file to configure as per your requirement based on the guidelines mentioned [here](https://docs.ansible.com/automation-controller/latest/html/userguide/ee_reference.html)
  

    **requirements.yml**
    ```yaml
    collections:
      - dellemc.openmanage
      - ansible.utils
      - ansible.windows
    ```
    Note: The content of the *requirements.yml* can be found [here](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/requirements.yml)

    **requirements.txt**
    ```yaml
    omsdk
    netaddr>=0.7.19
    ```

    Note: The content of the *requirements.txt* can be found [here](https://github.com/dell/dellemc-openmanage-ansible-modules/blob/collections/requirements.txt)

3. Build the Podman image using the following syntax:

    `ansible-builder build -f <path>/execution-environment.yml --container-runtime=<container> -c build_context --tag <container.io>/<org_name or username>/<imagename>:<tag>`

    In this tutorial, the following command is used to build the Docker image with the name "*execution-environment*".

    ```yaml
    $ ansible-builder build -f execution-environment.yml --container-runtime=podman -c build_context --tag quay.io/delluser/dell-openmanage-ee:<tag>

    podman build -f context/Containerfile -t quay.io/delluser/dell-openmanage-ee context
    Complete! The build context can be found at: /context
    ```

## Use Ansible Runner to verify the execution environment

**Note:** Using Ansible Runner to verify the execution environment is an optional step.

**Prerequisite**

Ensure to install Ansible Runner. For details on how to install Ansible Runner, see [https://ansible-runner.readthedocs.io/en/stable/install/](https://ansible-runner.readthedocs.io/en/stable/install/).

To verify the image using the Ansible Runner, do the following:

1. Create a folder structure as shown below:

```yaml
runner-example/
├── inventory
│   └── hosts   
└── project
    └── testplaybook.yml
```

2. Create a host file with the following entries:

```yaml
[idrac]
192.168.0.1

[idrac:vars]
ansible_python_interpreter=/usr/bin/python3.9
user=user
password=password
```
3. Create a playbook.

```yaml
- name: Get system inventory
  hosts: idrac
  gather_facts: false

  tasks:
    - name: Get system inventory.
      dellemc.openmanage.idrac_system_info:
        idrac_ip: "{{ inventory_hostname  }}"
        idrac_user: "{{ user }}"
        idrac_password:  "{{ password }}"
        validate_certs: false
      delegate_to: localhost
```
4. Run the playbook using the following command:

```yaml
ansible-runner run --process-isolation --process-isolation-executable podman --container-image quay.io/delluser/dell-openmanage-ee -p sysinfo.yml ./runner-example/ -v
No config file found; using defaults

PLAY [Get system inventory] ****************************************************

TASK [Get system inventory.] ***************************************************

ok: [192.168.0.1] => { ..sysdetails..}
META: ran handlers
META: ran handlers

PLAY RECAP *********************************************************************
192.168.0.1               : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
After the execution, a complete trace of execution information is saved in a directory structure as shown below: 

```yaml
# tree runner-example/
runner-example/
├── artifacts
│   └── 53810baa-15de-4dd6-93a1-35a28eb89070
│       ├── ansible_version.txt
│       ├── collections.json
│       ├── command
│       ├── env.list
│       ├── fact_cache
│       ├── job_events
│       │   ├── 1-592da7d5-b64f-4121-a91f-b33f28f6b0da.json
│       │   ├── 2-0242ac11-0007-b479-84c9-000000000006.json
│       │   ├── 3-0242ac11-0007-b479-84c9-000000000008.json
│       │   ├── 4-6d132edf-994c-4bf4-b9b2-dd6fa6ba834f.json
│       │   ├── 5-22b7e7a4-5244-4d3c-bbb7-395980feaee1.json
│       │   └── 6-c7e089be-6494-4b6e-8379-cf435e108aa6.json
│       ├── rc
│       ├── status
│       ├── stderr
│       └── stdout
├── inventory
│   └── hosts
└── project
└── sysinfo.yml
```
## Upload the execution environment to a registry

Now that you have built the image, you can upload the execution environment image to a registry. The following steps describe how to upload the image to a Docker registry. You can upload the image to a registry of your choice (https://quay.io or https://docker.io).

1. Log in to quay.io.
```yaml
podman login quay.io
```
2. To view the list of images, run the following command:

```yaml
podman image list
```   
Output:

```yaml
REPOSITORY                                      TAG       IMAGE ID       CREATED          SIZE
quay.io/delluser/dell-openmanage-ee             latest    6ea6337881f5   36 seconds ago   908MB
<none>                                          <none>    bab8f0c1f372   3 hours ago      959MB
<none>                                          <none>    26e61b6f31b6   3 hours ago      779MB
```
3. Upload the image to the repository using the following command:

```yaml
podman push quay.io/delluser/dell-openmanage-ee
```
Output:

```yaml
Using default tag: latest
The push refers to repository [quay.io/delluser/dell-openmanage-ee]
6a938007b4eb: Pushed
c1a7a8b69adb: Pushed
75f55eeed6f1: Pushed
7da4273e9d6b: Pushed
d8672b46fe52: Layer already exists
daf6e68722b8: Layer already exists
e258e2d51ae2: Layer already exists
134616f736b1: Layer already exists
34ac022ee9b6: Layer already exists
e7423a18eff2: Layer already exists
4d851e75ba42: Layer already exists
38adeed967d9: Layer already exists
78fc855ac59c: Layer already exists
d0f9b1e225dd: Layer already exists
5d4daec00137: Layer already exists
dd423f7aa20e: Layer already exists
1ce7e8b08eb8: Layer already exists
5fa5c1c78a8e: Layer already exists
e0808177f5c4: Layer already exists
aadc47c09f66: Layer already exists
101e6c349551: Layer already exists
latest: digest: sha256:7be5110235abf72e0547cac016a506d59313addefc445d35e5dff68edb0a9ad6 size: 4726
                                          <none>    26e61b6f31b6   3 hours ago      779MB
```

## Create execution environment in Ansible Automation Platform
Now that you uploaded the image to a registry, you can now create the execution environment in Ansible Automation Platform.  

### Add execution environment

1. Log in to Ansible Automation Platform.
2. On the navigation pane, click **Administration > Execution Environments**.
3. On the **Execution Environments** page, click **Add**.
4. On the **Create new execution environment** page, enter the following details, and click **Save**.
    - **Name**: Enter a name for the execution environment (required).
    - **Image**:  Enter the image name (required). The image name requires its full location (repo), the registry, image name, and version tag
    - **Pull**: From the **Pull** drop-down list, select **Only pull the image if not present before running**.
    - **Description**: optional.
    - **Organization**: optionally assign the organization to specifically use this execution environment. To make the execution environment available for use across multiple organizations, leave this field blank.
    - **Registry credential**: If the image has a protected container registry, provide the credential to access it.


### Create Projects

A Project is a logical collection of Ansible playbooks.

1.	On the navigation pane, click **Resources > Projects**.
2.	On the **Projects** page, click **Add**.
3.	On the **Create New Project** page, do the following, and click **Save**.
    -  From the **Source Control Credential Type** drop-down list, select the source control type. For example, you can select "GIT".
    -  In the **Source Control URL**, specify the source control URL. That is your repository link.

###   Create Credential Types   
This tutorial uses a custom credential type. You can create credential types depending on your data center environment. For more information, see [Credential Types](https://docs.ansible.com/automation-controller/4.2.1/html/userguide/credentials.html#credential-types). 

To create a credential type:

1. On the navigation pane, click **Administration > Credential Types**. 
2. On the **Credential Types** page, click **Add**.
2. On the **Create Credential Types** page, enter the name, and then specify the **Input configuration** and **Injector configuration**.
3. Click **Save**.

This tutorial uses a custom credential type. The following are the input configuration and injector configuration used in this tutorial.

**Input configuration:**

```yaml
fields:
  - id: username
    type: string
    label: Username
  - id: password
    type: string
    label: Password
    secret: true
required:
  - username
  - password
```

**Injector configuration:**

```yaml
extra_vars:
  user: '{{ username }}'
  password: '{{ password }}'
```
#### Create Credentials

1.	On the navigation pane, click **Resources > Credentials**.
2.	On the **Credentials** page, click **Add**.
3.	On the **Create New Credential** page, enter the name of the credential and select the credential type.
4. Click **Save**.

**Note:** In this tutorial, the custom credential type that we created in the section [Create Credential Types](#create-credential-types) is used.

## Create Inventories
1.	On the navigation pane, click **Resources > Inventories**.
2.	On the **Inventories** page, click **Add**.
3.	On the **Create New Inventory** page, enter the details and click **Save**.
4.	Add Groups and Hosts to the inventory.

## Create Job Templates

1.	On the navigation pane, click **Resources > Templates**.
2.	On the **Templates** page, click **Add** and select the new job template.
3.	On the **Create New Job Template** page, enter the name, inventory, project, execution environment, playbook, and credentials.
4.	Click **Save**.
5.	To run the template, on the **Details** page, click **Launch**.

To check the job status, on the navigation pane, select **Views  > Jobs**. The following is a sample output in JSON.

```yaml
PLAY [Get system inventory] ****************************************************

TASK [Get system inventory.] ***************************************************

ok: [192.168.0.1] => { ..sysdetails..}
META: ran handlers
META: ran handlers

PLAY RECAP *********************************************************************
192.168.0.1               : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Troubleshoot
You can add an Ansible python interpreter to a Template or Inventory.

`ansible_python_interpreter: /usr/bin/python<version>`

```yaml
ansible_python_interpreter: /usr/bin/python3.9
```

## Documentation references
- [https://www.redhat.com/en/technologies/management/ansible](https://www.redhat.com/en/technologies/management/ansible)
- [https://www.redhat.com/en/blog/what-ansible-automation-hub-and-why-should-you-use-it](https://www.redhat.com/en/blog/what-ansible-automation-hub-and-why-should-you-use-it)
- [https://www.ansible.com/blog/unlocking-efficiency-harnessing-the-capabilities-of-ansible-builder-3.0](https://www.ansible.com/blog/unlocking-efficiency-harnessing-the-capabilities-of-ansible-builder-3.0)
