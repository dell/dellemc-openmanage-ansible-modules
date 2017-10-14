# dellemc_idrac_power
Configure the Power Control options on a PowerEdge Server

  * Synopsis
  * Options
  * Examples

## Synopsis
Configure the Power Cycle options on a Dell EMC PowerEdge Server

## Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip   |  yes  |  | |  iDRAC IP Address |
| idrac_user |  yes  |  | |  iDRAC user name  |
| idrac_pwd  |  yes  |  | |  iDRAC user password  |
| idrac_port |  no  | 443 | |  iDRAC port number  |
| state  |   yes  |  | <ul> <li>PowerOn</li>  <li>SoftPowerCycle</li>  <li>SoftPowerOff</li>  <li>HardReset</li>  <li>DiagnosticInterrupt</li>  <li>GracefulPowerOff</li> </ul> |  <ul><li>if C(PowerOn), will Power On the server</li><li>if C(SoftPowerCycle), will close the running applications and Reboot the Server</li><li>if C(SoftPowerOff), will close the running applications and Power Off the server</li><li>if C(HardReset), will Reboot the Server immediately</li><li>if C(DiagnosticInterrupt), will reboot the Server for troubleshooting</li><li>if C(GracefulPowerOff), will close the running applications and Power Off the server</li></ul>  |
 
## Examples

```
# Power On
- name: Power On the Server
    dellemc_idrac_power:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      state:      "PowerOn"

# Graceful shutdown
- name: graceful shutdown
    dellemc_idrac_power:
      idrac_ip:   "192.168.1.1"
      idrac_user: "root"
      idrac_pwd:  "calvin"
      state:      "GracefulPowerOff"
```

---
Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
