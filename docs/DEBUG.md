<!--
Copyright (c) 2022 Dell Inc., or its subsidiaries. All Rights Reserved.

Licensed under the GPL, Version 3.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.gnu.org/licenses/gpl-3.0.txt
-->
# How to Perform Debugging

The following steps enables you to debug OpenManage Ansible Modules from an IDE either from local Linux or from a remote debugger on Windows.

1. Install OpenManage Ansible Modules from Galaxy `ansible-galaxy collection install dellemc.openmanage`. On Ubuntu this defaults to `$HOME/.ansible/collections/ansible_collections/dellemc/openmanage/` The problem with this is that this location is not in PYTHONPATH which will cause problems with the debugger.
2. To resolve python path issues,  move the `openmanage ` collection to align with the rest of Dell's code which is in PYTHONPATH with `sudo mv $HOME/.ansible/collections/ansible_collections/dellemc/openmanage/ /usr/local/lib/python3.X/dist-packages/ansible_collections/dellemc/`. The path may be different on your system, but it should be placed with your other python packages.
   Alternatively, you can add the directory `$HOME/.ansible/collections/ansible_collections/dellemc/openmanage/` to PYTHONPATH with `export PYTHONPATH=$PYTHONPATH:$HOME/.ansible/collections`.
    1. The location may be different for but the key is `openmanage` must be accessible within the `ansible_collections.dellemc` namespace. That is to say, the path should look like `<SOME_PREFIX (usually dist-packages)>/ansible_collections/dellemc/openmanage`
    2. Sometimes, `from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError` still reports an error. This error can be ignored safely.
    3. Some IDEs may require a restart in order to rescan the available packages for import statements to resolve.
3. Create a file with any name. We will use `args.json`. Fill it with the arguments you wish to provide to the module:

        {
            "ANSIBLE_MODULE_ARGS": {
                "idrac_ip": "192.168.1.63",
                "idrac_user": "root",
                "idrac_password": "password",
                "share_name": "some_share",
                "share_user": "some_username",
                "share_password": "some_password"
            }
        }

For more information about injecting arguments , see  the Ansible [docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#exercising-module-code-locally).

4. Execute one of the modules by running `python -m ansible.modules.<some_module> /tmp/args.json`.

How to run this in an IDE is described below.

## PyCharm

### On Remote Windows

The following steps helps to run and debug OpenManage Ansible Modules installed on the Linux VM using a remote debugger configured on Windows PyCharm IDE.

1. Download a copy of [the code](https://github.com/dell/dellemc-openmanage-ansible-modules) and open the folder with PyCharm.
2. Go to File->Settings->Project:<name_of_your_project>->Python Interpreter
3. Click the gear and then click add
4. Use `SSH Interpreter` and then add the Linux box mentioned above or another remote target of your choice.

### On Local Linux

1. You will need to configure the IDE to use the `args.json` file you created above. In PyCharm do this by going to Run-Edit Configurations. In `Parameters` add `<ABSOLUTE_PATH>\args.json`.  This will pass the JSON file as an argument to the module when it runs. You should now be able to debug the module directly.
2. It is also possible to pass the arguments within the Python script itself by updating the `main` function with:

        basic._ANSIBLE_ARGS = to_bytes(json.dumps({'ANSIBLE_MODULE_ARGS': {"idrac_ip": "192.168.0.1", "idrac_user": "username", "idrac_password": "password"}}))
        set_module_args(args)

3. If you would like to set PYTHONPATH with PyCharm you can do that by going to Run->Edit Configurations->Environment Variables and add 'PYTHONPATH=$PYTHONPATH:$HOME/.ansible/collections/'.
