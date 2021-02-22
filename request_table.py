#coding=utf-8
import sys
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

sys.exit()