# idrac_job_queue

 Role to manage the iDRAC(iDRAC8 and iDRAC9 only) lifecycle controller job queue. 

## Requirements

### Development
Requirements to develop and contribute to the role.
```
ansible
docker
molecule
python
```
### Production
Requirements to use the role.
```
ansible
python
```

### Ansible collections
Collections required to use the role
```
dellemc.openmanage
```

## Role Variables

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Required</th>
    <th>Default Value</th>
    <th>Choices</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>hostname</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC IP Address</td>
  </tr>
  <tr>
    <td>username</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC username</td>
  </tr>
  <tr>
    <td>password</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC user password.</td>
  </tr>
  <tr>
    <td>https_port</td>
    <td>false</td>
    <td>443</td>
    <td></td>
    <td>int</td>
    <td>- iDRAC port.</td>
  </tr>
  <tr>
    <td>validate_certs</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- If C(false), the SSL certificates will not be validated.<br>- Configure C(false) only on personally controlled sites where self-signed certificates are used.</td>
  </tr>
  <tr>
    <td>ca_path</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>- The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.</td>
  </tr>
  <tr>
    <td>https_timeout</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td>- The HTTPS socket level timeout in seconds.</td>
  </tr>
  <tr>
    <td>clear_job_queue</td>
    <td>false</td>
    <td>false</td>
    <td></td>
    <td>bool</td>
    <td>- Clears the job queue of the iDRAC.</td>
  </tr>
  <tr>
    <td>job_id</td>
    <td>false</td>
    <td>false</td>
    <td></td>
    <td>str</td>
    <td>- Id of the job to be deleted.<br>- If I(clear_job_queue) is C(true) then the I(job_id) will be ignored.</td>
  </tr>
  <tr>
    <td>force</td>
    <td>false</td>
    <td>false</td>
    <td></td>
    <td>bool</td>
    <td>- Clears the job queue of the iDRAC forcefully.</td>         
  </tr>
</tbody>
</table>

## Fact variables

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Sample</th>
    <th>Description</th>
  </tr>
</thead>
  <tbody>
    <tr>
      <td>idrac_job_queue_out</td>
      <td>{msg: "The job queue can been cleared successfully"
}</td>
<td>Module output of idrac job queue</td>
</tbody>
</table>

## Examples 
-----

```
- name: Delete a Job
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_job_queue:         
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    job_id: JID_XXXXXXXXXXXX  
 
- name: Clear the job queue
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_job_queue:         
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    clear_job_queue: true
 
- name: Clear the job queue forcefully
  ansible.builtin.include_role:
    name: dellemc.openmanage.idrac_job_queue:         
  vars:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    clear_job_queue: true
    force: true
```

## Author Information
------------------

Dell Technologies <br>
Kritika Bhateja (Kritika.Bhateja@Dell.com)  2023
