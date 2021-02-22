# Python-ARP-Tools
[![python](https://github.takahashi65.info/lib_badge/python.svg)](https://www.python.org/)
[![python version](https://github.takahashi65.info/lib_badge/python-3.6.svg)](https://www.python.org/) 
[![UA](https://github.takahashi65.info/lib_badge/active_maintenance.svg)](https://github.com/Suzhou65/Python-ARP-Tools)
[![Size](https://github-size-badge.herokuapp.com/Suzhou65/Python-ARP-Tools.svg)](https://github.com/axetroy/github-size-badge)

Using Python asking router ARP, export to csv format data, or checking specify device is on ARP list or not, and trying to added back.

## Contents
- [Python-ARP-Tools](#python-arp-tools)
  * [Contents](#contents)
  * [Configuration file](#configuration-file)
  * [Usage](#usage)
    + [Telnet function configure](#telnet-function-configure)
    + [Device placeholder](#device-placeholder)
    + [MAC address format](#mac-address-format)
    + [Difference between Traditional router and Mesh router](#difference-between-traditional-router-and-mesh-router)
  * [Import module](#import-module)
  * [Function](#function)
    + [Directly export router ARP to csv file](#directly-export-router-arp-to-csv-file)
    + [ARP to tidy csv file](#arp-to-tidy-csv-file)
    + [ARP Overwatch](#arp-overwatch)
  * [Output format](#output-format)
    + [Raw ARP](#raw-arp)
    + [Tidy ARP](#tidy-arp)
    + [ARP Overwatch](#arp-overwatch-1)
  * [Dependencies](#dependencies)
    + [Python version](#python-version)
    + [Python module](#python-module)
  * [License](#license)
  * [Resources](#resources)

## Configuration file
ARP-Tools store configuration as JSON format file, named ```config.json```.

You can editing the clean copy, which looks like this:
```json
{
  "last_update_time": "",
  "server": "192.168.0.1",
  "user_prompt":"login:",
  "user": "admin",
  "password_prompt":"Password:",
  "password": "•••••••••••••••",
  "terminal_prompt": "user@router:/# ",
  "command":"arp",
  "interface_prompt":"-s",
  "filter_list":[],
  "device_ip": "",
  "device_mac_address":""
}
```

## Usage
For using this module, you need to have a domain name, and choice CloudFlare as the DNS hosting services.

Logged in the Cloudflare Dashboard, and go to User Profile, choice [API Tokens](https://dash.cloudflare.com/profile/api-tokens), generated API Token. **Once successfully generated, the token secret is only shown once**, make sure to copy the secret to a secure place. 

This module needs some configuration which is necessary.

### Telnet function configure
[Telnet function](https://openwrt.org/toh/netgear/telnet.console) is the alternative solution for NETGEAR official firmware, If you know what is [DD-WRT](https://forum.dd-wrt.com/wiki/index.php/Main_Page) and luckily your router is under support list, try [commond line function](https://wiki.dd-wrt.com/wiki/index.php/Telnet/SSH_and_the_Command_Line).

Python Telnet function using telnetlib, which need some necessery configure, which store at ```config.json```.

If the configuration file not found, it will needed to initialize
```text
Configuration not found, please initialize.

Please enter the Server IP address: 192.168.01.1
Please enter the prompt when asking username: login: 
Please enter the username: admin
Please enter the prompt when asking password: Passowrd:
Please enter the password: •••••••••••••••
Please setting the telnet prompt: user@router:/# 
Please enter the device IP address (can be skipped):
Please enter the device MAC address (can be skipped):
```
- Server IP address is the address for your router, store key is ```server```
- Prompt when asking username is the prompt when typing username, store key is ```user_prompt```
- User is the administrator's username, usually is admin, store key is ```user```
- Prompt when asking password is the prompt when typing password, store key is ```password_prompt```
- Password is the administrator's password, store key is ```password```
- Telnet prompt depend on you router hostname and prompt, store key is ```terminal_prompt```.

The parameter depend on you router hostname and prompt, in my condition, my NETGEAR router is ```root@RBS50:/# ```, DD-WRT default is ```root@DDWRT:/# ```. **Blank character at the ending are needed.**

### Device placeholder
If you wnat to keep specify device on ARP list, you need to complete the configuration.
```text
Please enter the device IP address (can be skipped):
Please enter the device MAC address (can be skipped):
```
- Device IP address is the specify device IP address, store key is ```device_ip```
- Device MAC address is the specify device MAC address, store key is ```device_mac_address```

To processing ARP data into dataframe correctly, ```filter_list``` need to configure. First directly export ARP data, check the output file ```arp_format_check.csv``` to know which columns needs to drop, then set ```filter_list``` value to ```List```. For example:
```json
"filter_list":[6,7,8],
```

Network interface and ARP command format may quite different on different platform or device, check you environments, then modify the parameter.
```json
"interface_prompt":"-s",
```

### MAC address format
Base on different platform or device, even different firmware version, the MAC address format may quite different.

Default trans MAC address into lower-case
```python
#Trans ARP list into lowercase
comparison_list = [x.lower() for x in comparison_list]
#Try to match
if device_keep.lower() in comparison_list:
```
In my condition, my router store MAC address in lower-case, and the separate character using ``` : ```

### Difference between Traditional router and Mesh router
Base on different platform or device, even different firmware version, ARP refresh times are different, and traditional routers are quite different from Mesh Wi-Fi.

For example, NETGEAR Orbi AC3000 system, RBR50 main station and RBS50 satellite station has **separated ARP cache**, so careful, Mesh Wi-Fi environments may not be compatible.

## Import module
- Import the module
```python
import arp_tools
```
- Alternatively, you can import the function independent
```python
from arp_tools import arp_output
```

## Function
### Directly export router ARP to csv file
```python
import arp_tools
#Run asking
result = arp_tools.arp_output(directly_mode=True)
#Check result
if result is None:
    print("ARP data dumping fail, error occurred during data processing.\r\nPlease check the error.log")
elif type(result) is bool:
    if bool(result) is True:
        print("Router connection refused.")
    elif bool(result) is False:
        print("Error occurred when connect to router.\r\nPlease check the error.log")
else:
    print("ARP data save as 'arp_format_check.csv'.")
```
If the telnet function successfully login, and asking data, the result will print.
```text
Login Router ...
Login success
Sending ARP request to router
Receive ARP data from router
Logout Router ...
2021-02-22 10:16:07 | ARP data dump complete
ARP data save as 'arp_format_check.csv'.
```
If error occurred, it will return ```Boolean ``` or ```None``` as the result.

### ARP to tidy csv file
```python
import arp_tools
#Run asking
result = arp_tools.arp_output(directly_mode=False)
#Check result
if result is None:
    print("ARP data dumping fail, error occurred during data processing.\r\nPlease check the error.log")
elif type(result) is bool:
    if bool(result) is True:
        print("Router connection refused.")
    elif bool(result) is False:
        print("Error occurred when connect to router.\r\nPlease check the error.log")
else:
    print("ARP data save as 'arp_data_output.csv'.")
```
If the telnet function successfully login, and asking data, the result will print.
```text
Login Router ...
Login success
Sending ARP request to router
Receive ARP data from router
Logout Router ...
2021-02-22 10:17:48 | ARP data dump complete
ARP data save as 'arp_data_output.csv'.
```
If error occurred, it will return ```Boolean ``` or ```None``` as the result.

### ARP Overwatch
Checking specify device is on ARP list or not, and trying to added back.
```python
import arp_tools
#Run asking
result = arp_tools.arp_overwatch()
#Check result
if result is None:
    print("ARP data dumping fail, error occurred during data processing.\r\nPlease check the error.log")
elif type(result) is int:
    print("ARP update command has been amended.")
elif type(result) is str:
    print("No needed to update.")
elif type(result) is bool:
    if bool(result) is True:
        print("Router connection refused.")
    elif bool(result) is False:
        print("Error occurred when connect to router.\r\nPlease check the error.log")
```
If the telnet function successfully login, and need to update ARP, the result will print.
```text
Initialization, event log create
Login Router ...
Login success
Sending ARP request to router
Receive ARP data from router
2021-02-21 22:43:24 | Update
Logout
```
It will return ```integer``` as the result.

If the device already on ARP table, the result will print.
```text
Login Router ...
Login success
Sending ARP request to router
Receive ARP data from router
2021-02-21 22:43:27 | Device already on the list
Logout
```
It will return ```string``` as the result.  
If error occurred, it will return ```Boolean ``` or ```None``` as the result.

## Output format
### Raw ARP
Directly export ARP data will store at ```arp_format_check.csv``` :
```csv
IP,address,HW,type,Flags,HW.1,address.1,Mask,Device
10.0.1.7,0x1,0x2,2e:07:75:cc:9d:01,*,br0,,,
10.0.1.6,0x1,0x2,5e:bd:ef:3c:38:35,*,br0,,,
10.0.1.15,0x1,0x2,26:ff:10:f0:6e:2a,*,br0,,,
```
### Tidy ARP
The ARP data after processing will store at ```arp_data_output.csv``` :
```csv
IP address,HW type,Flags,HW address,Mask,Device
10.0.1.19,0x1,0x2,2e:07:75:cc:9d:01,*,br0
10.0.1.15,0x1,0x2,26:ff:10:f0:6e:2a,*,br0
10.0.1.6,0x1,0x2,5e:bd:ef:3c:38:35,*,br0
```
### ARP Overwatch
The ARP Check/Update event will store at ```arp_placeholder.csv``` :
```csv
time,event
2021-01-17 20:07:55,check
2021-01-17 20:08:01,update
```

## Dependencies
### Python version
- Python 3.6 or above

### Python module
- csv
- json
- time
- pandas
- logging
- datetime
- telnetlib
- io
- getpass

## License
General Public License -3.0

## Resources
- [GitHub, python_arptable](https://github.com/XayOn/python_arptable)
- [DD-WRT Wiki, Obtaining Router IP](https://wiki.dd-wrt.com/wiki/index.php/Obtaining_Router_IP)
- [DD-WRT Wiki, Remote Wake On LAN via Port Forwarding](https://wiki.dd-wrt.com/wiki/index.php/WOL#Remote_Wake_On_LAN_via_Port_Forwarding)
