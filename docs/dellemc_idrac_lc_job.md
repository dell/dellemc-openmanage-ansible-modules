# dellemc_idrac_lc_job
Get the status of a Lifecycle Controller Job, delete a LC Job

  * [Synopsis](#Synopsis)
  * [Options](#Options)
  * [Examples](#Examples)

## <a name="Synopsis"></a>Synopsis
  * Get the status of a Lifecycle Controller job given valid a JOB ID
  * Delete a LC Job from the Job queue given a valid JOB ID
  * Delete LC Job Queue

## <a name="Options"></a>Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   yes  |  | |  iDRAC IP Address  |
| idrac_user  |   yes  |  | |  iDRAC user name  |
| idrac_pwd  |   yes  |  | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| job_id  |   yes  |  | |  <ul><li>JOB ID in the format JID_123456789012</li><li>if C(JID_CLEARALL), then all jobs will be cleared from the LC job queue</li></ul>  |
| state  |   no  |  present  | |  <ul><li>if C(present), returns the status of the associated job having the job id provided in I(job_id)</li><li>if C(present) and I(job_id) == C(JID_CLEARALL), then delete the job queue</li><li>if C(absent), then delete the associated job having the job id provided in I(job_id) from LC job queue</li></ul> |
 
## <a name="Examples"></a>Examples

```
# Get Job Status for a valid JOB ID
- name: Get LC Job Stattus
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"
      state:      "present"
```

```
# Delete the JOB from the LC Job Queue
- name: Delete the LC Job
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_1234556789012"
      state:      "absent"
```

```
# Clear the LC Job queue
- name: Clear the LC Job queue
    dellemc_idrac_lc_job:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      job_id:     "JID_CLEARALL"
      state:      "present"
```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
