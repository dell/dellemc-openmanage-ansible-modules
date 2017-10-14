# dellemc_idrac_web_server
Configure iDRAC Web Server service interface settings

  * Synopsis
  * Options
  * Examples

## Synopsis
 Configure iDRAC Web Server Service interface settings such as minimum supprted levels of Transport Layer Security (TLS) protocol and levels of Secure Socket Layer (SSL) Encryption

## Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| idrac_ip  |   no  |    | |  iDRAC IP Address  |
| idrac_user  |   no  |    | |  iDRAC user name  |
| idrac_pwd  |   no  |    | |  iDRAC user password  |
| idrac_port  |   no  |  443  | |  iDRAC port  |
| share_name  |   yes  |  | |  Network file share  |
| share_user  |   yes  |  | |  Network share user in the format user@domain  |
| share_pwd  |   yes  |  | |  Network share user password  |
| share_mnt  |   yes  |  | |  Local mount path of the network file share with read-write permission for ansible user  |
| http_port  |   no  |  80  | |  iDRAC Web Server HTTP port  |
| https_port  |   no  |  443  | |  iDRAC Web Server HTTPS port  |
| timeout  |   no  |  1800  | |  Time (in seconds) that a connection is allowed to remain idle  Changes to the timeout settings do not affect the current session  If you change the timeout value, you must log out and log in again for the new settings to take effect  Timeout range is 60 to 10800 seconds  |
| tls_protocol  |   no  |  TLS 1.1 and Higher  | <ul> <li>TLS 1.0 and Higher</li>  <li>TLS 1.1 and Higher</li>  <li>TLS 1.2 Only</li> </ul> |  if C(TLS 1.0 and Higher), will set the TLS protocol to TLS 1.0 and higher  if C(TLS 1.1 and Higher), will set the TLS protocol to TLS 1.1 and higher  if C(TLS 1.2 Only), will set the TLS protocol option to TLS 1.2 Only  |
| ssl_bits  |   no  |  128-Bit or higher  | <ul> <li>Auto-Negotiate</li>  <li>128-Bit or higher</li>  <li>168-Bit or higher</li>  <li>256-Bit or higher</li> </ul> |  if C(128-Bit or higher), will set the SSL Encryption Bits to 128-Bit or higher  if C(168-Bit or higher), will set the SSL Encryption Bits to 168-Bit or higher  if C(256-Bit or higher), will set the SSL Encryption Bits to 256-Bit or higher  if C(Auto-Negotiate), will set the SSL Encryption Bits to Auto-Negotiate  |
| state  |   no  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  if C(present), will enable the Web Server and configure the Web Server parameters  if C(absent), will disable the Web Server. Please note that you will not be able to use the iDRAC Web Interface if you disable the Web server.  |

 
## Examples

```
- name: Configure Web Server TLS and SSL settings (using CIFS network share)
    dellemc_idrac_web_server:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\192.168.10.10\share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      tls_protocol: "TLS 1.2 Only"
      ssl_bits:     "256-Bit or higher"

- name: Configure Web Server TLS and SSL settings (using NFS network share)
    dellemc_idrac_web_server:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "192.168.10.10:/share"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      tls_protocol: "TLS 1.2 Only"
      ssl_bits:     "256-Bit or higher"

```

---

Copyright © 2017 Dell Inc. or its subsidiaries. All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries. Other trademarks may be trademarks of their respective owners.
