# Python-ARP-Tools
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/Python-ARP-Tools)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/Python-ARP-Tools.svg)](https://github.com/axetroy/github-size-badge)

Using Python asking router ARP, export to csv format data, or checking specify device is on ARP list or not, and trying to added back.

## Contents
- [Python-ARP-Tools](#python-arp-tools)
  * [Usage](#usage)
    + [Telnet function](#telnet-function)
    + [ARP format and command](#arp-format-and-command)
    + [MAC address format](#mac-address-format)
    + [Difference between Traditional router and Mesh router](#difference-between-traditional-router-and-mesh-router)
  * [Python module](#python-module)
  * [Function](#function)
    + [ARP table format checker](#arp-table-format-checker)
    + [ARP to CSV](#arp-to-csv)
    + [ARP Overwatch](#arp-overwatch)
  * [Output format](#output-format)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module-1)
  * [License](#license)
  * [Resources](#resources)

## Usage
For using this module, you need to have a domain name, and choice CloudFlare as the DNS hosting services.

Logged in the Cloudflare Dashboard, and go to User Profile, choice [API Tokens](https://dash.cloudflare.com/profile/api-tokens), generated API Token. **Once successfully generated, the token secret is only shown once**, make sure to copy the secret to a secure place. 

This module needs some configuration which is necessary.

### Telnet function
[Telnet function](https://openwrt.org/toh/netgear/telnet.console) is the alternative solution for NETGEAR official firmware, If you know what is [DD-WRT](https://forum.dd-wrt.com/wiki/index.php/Main_Page) and luckily your router is under support list, try [commond line function](https://wiki.dd-wrt.com/wiki/index.php/Telnet/SSH_and_the_Command_Line).

Python Telnet function using telnetlib, which is standard library. **Also**, the telnetlib function parameter depend on you router hostname and prompt.
```python
#Telnet
user = "admin"
password = "KOKOSUKI"
server = "114.514.19.19"

#Telnet prompt, Bytes string [user@hostname:/# ] related to tn.read_until section
prompt = b"root@YJSP:/# "
```
- **user** is the administrator's username, usually is **admin**.
- **password** is the administrator's password.
- **server** is the address for your router.
- **prompt** depend on you router hostname and prompt.

### ARP format and command
Code development base on **Qualcomm** Networking Platform, in this project I was using NETGEAR Orbi AC3000 system. **Base on different platform or device, even different firmware version, the ARP format may quite different.**

The function **format_checker** will directly export ARP cache to csv format data, you can check the output file, **arp_format_check.csv** can let you know which columns needs to drop.

ARP command format may quite different on different platform or device, check you environments, then modify the parameter.
```python
#Columns unnecessary
remove_columns = [6,7,8]

#Device
device_ip = "114.514.19.810"
device_mac = "06:AA:A3:2E:4D:86"
```
- **remove_columns** is the list depend on you router ARP output format.
- **device_ip** is the IP address you wnat to keep the device on it.
- **device_mac** is the device's MAC address.

You also need to modify this function, depend on you router ARP output format
```python
#ARP update command
def update(device_ip, device_mac):
    return "arp -i br0 -s" + " " + device_ip + " " + device_mac
```

### MAC address format
**Base on different platform or device, even different firmware version, the MAC address format may quite different.**
```python
#Trans ARP list into lowercase
comparison_list = [x.lower() for x in comparison_list]

#Match
if device_mac.lower() in comparison_list:
```
In this module, all MAC address will trans into the lowercase, and the separate character using " : "

### Difference between Traditional router and Mesh router
Base on different platform or device, even different firmware version, ARP refresh times are different, and traditional routers are quite different from Mesh Wi-Fi.

For example, NETGEAR Orbi AC3000 system, RBR50 main station and RBS50 satellite station has **separated ARP cache**, so careful, Mesh Wi-Fi environments may not be compatible.

## Python module
- Import the module
```python
import arp_tools
```
- Alternatively, you can import the function independent
```python
from arp_tools import format_checker
```

## Function
### ARP table format checker
Directly export router ARP to csv format data.
```python
from arp_tools import format_checker
output = format_checker(user, password, server, prompt)
```
If the telnet function successfully login, and asking data, the result will print.
```text
Login
Login success
Sending ARP asking request
Receive ARP data
Logout
2021-01-17 20:07:42 | ARP data dump complete
```
If error occurred, it will return massage at the values.

### ARP to CSV
Using Python asking router ARP, export to csv format data.
```python
import arp_tools import arp2csv
output = arp2csv(user, password, server, prompt, remove_columns)
```
If the telnet function successfully login, and asking data, the result will print.
```text
Login
Login success
Sending ARP asking request
Receive ARP data
Logout
2021-01-17 20:07:49 | ARP data file save complete
```
If error occurred, it will return massage at the values.

### ARP Overwatch
ARP overwatch, checking specify device is on ARP list or not, and trying to added back.
```python
from arp_tools import arp_overwatch
check = arp_overwatch(user, password, server, prompt, remove_columns, device_ip, device_mac)
```
If the telnet function successfully login, and need to update ARP, the result will print.
```text
Initialization
Login
Login success
Sending ARP asking request
Receive ARP data
2021-01-17 20:08:01 | Update
Logout
```
It will also return event's time by string.

If the device already on ARP table, the result will print.
```text
Initialization
Login
Login success
Sending ARP asking request
Receive ARP data
2021-01-17 20:07:55 | Device already on the list
Logout
```
It will also return event's time by string.

If error occurred, it will return massage at the values.

## Output format
### ARP table format checker
This is an example show how the format looks likes if directly export it.
```csv
IP,address,HW,type,Flags,HW.1,address.1,Mask,Device
10.0.1.7,0x1,0x2,2e:07:75:cc:9d:01,*,br0,,,
10.0.1.6,0x1,0x2,5e:bd:ef:3c:38:35,*,br0,,,
10.0.1.15,0x1,0x2,26:ff:10:f0:6e:2a,*,br0,,,
```

### ARP to CSV
This is an example show how the format looks likes after processing.
```csv
IP address,HW type,Flags,HW address,Mask,Device
10.0.1.19,0x1,0x2,2e:07:75:cc:9d:01,*,br0
10.0.1.15,0x1,0x2,26:ff:10:f0:6e:2a,*,br0
10.0.1.6,0x1,0x2,5e:bd:ef:3c:38:35,*,br0
```

### ARP Overwatch
The ARP Check/Update event will record looks likes this.
```csv
time,event
2021-01-17 20:07:55,check
2021-01-17 20:08:01,update
```

## Dependencies
### Python version
Python 3.6 or above.

### Python module
- os
- sys
- io
- time
- telnetlib
- datetime
- csv
- pandas

## License
General Public License -3.0

## Resources
- [GitHub, python_arptable](https://github.com/XayOn/python_arptable)
- [DD-WRT Wiki, Obtaining Router IP](https://wiki.dd-wrt.com/wiki/index.php/Obtaining_Router_IP)
- [DD-WRT Wiki, Remote Wake On LAN via Port Forwarding](https://wiki.dd-wrt.com/wiki/index.php/WOL#Remote_Wake_On_LAN_via_Port_Forwarding)
