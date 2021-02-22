#coding=utf-8
import csv
import json
import time
import pandas
import logging
import datetime
import telnetlib
from io import StringIO
from getpass import getpass

#Error logging
FORMAT = "%(asctime)s |%(levelname)s |%(message)s"
logging.basicConfig(level=logging.WARNING, filename="error.log", filemode="a", format=FORMAT)

#Time
def current_time():
    today = datetime.datetime.now()
    return today.strftime('%Y-%m-%d %H:%M:%S')

#Configuration
def configuration( update_config=() ):
    if bool(update_config) is False:
        #Reading configuration file
        try:
            with open("config.json", "r") as configuration_file:
                #Return dictionary
                return json.load(configuration_file)
        #If file not found
        except FileNotFoundError:
            #Stamp
            time_initialize = current_time()
            #Initialization
            print("Configuration not found, please initialize.\r\n")
            #Server address
            server = input("Please enter the Server IP address: ")
            user_prompt = input("Please enter the prompt when asking username: ")
            user = input("Please enter the username: ")
            password_prompt = input("Please enter the prompt when asking password: ")
            password = getpass("Please enter the password: ")
            #Telnet prompt, Bytes string [] related to tn.read_until section
            terminal_prompt = input("Please setting the telnet prompt: ")
            #ARP overwatch
            device_ip = input("Please enter the device IP address (can be skipped): ")
            device_mac_address = input("Please enter the device MAC address (can be skipped): ")
            #Dictionary
            initialize_config = {
                "last_update_time":time_initialize,
                "server":server,
                "user_prompt":user_prompt,
                "user":user,
                "password_prompt":password_prompt,
                "password":password,
                "terminal_prompt":terminal_prompt,
                "command":"arp",
                "filter_list":"",
                "device_ip":device_ip,
                "device_mac_address":device_mac_address
                }
            #Save configuration file
            with open("config.json", "w") as configuration_file:
                json.dump(initialize_config, configuration_file, indent=2)
                print("Configuration saved successfully.")
                #Return dictionary after initialize
                return initialize_config
    #Update configuration file
    elif bool(update_config) is True:
        with open("config.json", "w") as configuration_file:
            json.dump(update_config, configuration_file, indent=2)
            #Return dictionary after update
            return update_config

#Data processing
def printing_result(data_receive, filter_mode=() ):
    #Read configuration file
    telnet_config = configuration(update_config=False)
    #Bytes string related to tn.read_until section
    prompt_end = telnet_config["terminal_prompt"]
    #ARP command string
    command_start = telnet_config["command"]
    #Get filter columns
    filter_columns = telnet_config["filter_list"]
    try:
        #Directly
        if bool(filter_mode) is False:
            #Remove commond and telnet header
            str_arp = data_receive.replace(command_start,"").replace(prompt_end,"")
            #Trans telnetlib into pandas dataframe
            result_directly = pandas.read_csv(StringIO(str_arp), skip_blank_lines=True, sep=r'\s+', skipinitialspace=False)
            return result_directly
        #Procress telnet output
        elif bool(filter_mode) is True:
            #Remove commond and telnet header
            str_arp = data_receive.replace(command_start,"").replace(prompt_end,"")
            #Trans telnetlib into pandas dataframe
            arp_tb = pandas.read_csv(StringIO(str_arp), skip_blank_lines=True, sep=r'\s+', skipinitialspace=False)
            #Drop dataframe columns
            if len(filter_columns) == 0:
                print("Filter columns isn't set correctly!\r\n")
                print("Please using arp_table_output(directly_mode=True) to know which columns needs to drop.")
                return None
            else:
                #Using arp_table_output(directly_mode=True) 
                arp_db = arp_tb.drop(arp_tb.columns[filter_columns], axis=1, inplace = False)
                #Setting header
                result_dataframe = arp_db.set_axis(['IP address', 'HW type', 'Flags', 'HW address', 'Mask', 'Device'], axis=1, inplace=False)
                return result_dataframe
    except Exception as error_status:
        logging.exception(error_status)
        return None

#Dump ARP
def arp_output(directly_mode=() ):
    #Read configuration file
    telnet_config = configuration(update_config=False)
    #Telnet configuration
    connect_server = telnet_config["server"]
    asking_username = telnet_config["user_prompt"]
    username = telnet_config["user"]
    asking_password = telnet_config["password_prompt"]
    password = telnet_config["password"]
    waiting_command = telnet_config["terminal_prompt"]
    input_command = telnet_config["command"]
    #Translate header string into bytes
    prompt = waiting_command.encode()
    #Translate asking into bytes
    prompt_login = asking_username.encode()
    prompt_authy = asking_password.encode()
    #Connecting
    try:
        #Start
        tn = telnetlib.Telnet(connect_server)
        #telnet account:
        tn.read_until(prompt_login)
        print("Login Router ...")
        tn.write(username.encode('ascii') + b"\n")
        time.sleep(1)
        tn.read_until(prompt_authy)
        time.sleep(1)
        tn.write(password.encode('ascii') + b"\n")
        print("Login success")
        #Asking ARP data
        time.sleep(1)
        tn.read_until(prompt)
        tn.write(input_command.encode('ascii') + b"\n")
        print("Sending ARP request to router")
        #Receive data
        time.sleep(3)
        data_receive = tn.read_until(prompt).decode('ascii')
        print("Receive ARP data from router")
        #Close telnet connect
        time.sleep(1)
        tn.write("exit".encode('ascii') + b"\n")
        tn.close()
        print("Logout Router ...")
        #Save data to csv file
        time_print = current_time()
        #Dump ARP table directly
        if bool(directly_mode) is True:
            arp_asking_result = printing_result(data_receive, filter_mode=False)
            if arp_asking_result is None:
                print(f"{time_print} | ARP data dump Fail")
                return None
            else:
                arp_asking_result.to_csv("arp_format_check.csv", index=False)
                print(f"{time_print} | ARP data dump complete")
                return arp_asking_result
        #Dump ARP table after filter
        elif bool(directly_mode) is False:
            arp_asking_result = printing_result(data_receive, filter_mode=True)
            if arp_asking_result is None:
                print(f"{time_print} | ARP data dump Fail")
                return None
            else:
                arp_asking_result.to_csv("arp_result.csv", index=False)
                print(f"{time_print} | ARP data dump complete")
                return arp_asking_result
    #If ConnectionRefusedError
    except ConnectionRefusedError as connect_refuse:
        logging.warning(connect_refuse)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False

#ARP placeholder
def arp_overwatch():
    #Create record file
    try:
        #If exist, end check process
        with open("arp_placeholder.csv", mode="r") as book:
            print("Initialization")
            book.close()
    except FileNotFoundError:
        #If not exist, create it
        with open("arp_placeholder.csv", mode="w") as event:
            create = csv.writer(event, delimiter=",")
            create.writerow(["time","event"])
            print("Initialization, event log create")
    #Read configuration file
    telnet_config = configuration(update_config=False)
    #Telnet configuration
    connect_server = telnet_config["server"]
    asking_username = telnet_config["user_prompt"]
    username = telnet_config["user"]
    asking_password = telnet_config["password_prompt"]
    password = telnet_config["password"]
    waiting_command = telnet_config["terminal_prompt"]
    input_command = telnet_config["command"]
    #Device keeping
    device_keep = telnet_config ["device_mac_address"]
    placeholder = telnet_config ["device_ip"]
    #Translate header string into bytes
    prompt = waiting_command.encode()
    #Translate asking into bytes
    prompt_login = asking_username.encode()
    prompt_authy = asking_password.encode()
    #ARP update command
    update_prompt = telnet_config["interface_prompt"]
    update_command = input_command + " " + update_prompt + " " + placeholder + " " + device_keep
    #Connecting
    try:
        with open("arp_placeholder.csv", mode="a") as event_log:
            booking=csv.writer(event_log)
            #Start
            tn = telnetlib.Telnet(connect_server)
            tn.read_until(prompt_login)
            print("Login Router ...")
            tn.write(username.encode('ascii') + b"\n")
            time.sleep(1)
            tn.read_until(prompt_authy)
            time.sleep(1)
            tn.write(password.encode('ascii') + b"\n")
            print("Login success")
            #Asking ARP data
            time.sleep(1)
            tn.read_until(prompt)
            tn.write(input_command.encode('ascii') + b"\n")
            print("Sending ARP request to router")
            #Receive data
            time.sleep(3)
            data_receive = tn.read_until(prompt).decode('ascii')
            print("Receive ARP data from router")
            #Wait
            time.sleep(1)
            #Comparison
            comparison = printing_result(data_receive, filter_mode=True)
            if comparison is None:
                warning = "ARP data processing error"
                print(warning)
                logging.warning(warning)
                return None
            else:
                comparison_list = comparison["HW address"].tolist()
                #Trans ARP list into lowercase
                comparison_list = [x.lower() for x in comparison_list]
                #Try to match
                if device_keep.lower() in comparison_list:
                    #If device already on ARP
                    time_macth = current_time()
                    booking.writerow([time_macth,"check"])
                    print(f"{time_macth} | Device already on the list")
                    #Close telnet connect
                    tn.write("exit".encode('ascii') + b"\n")
                    tn.close()
                    print("Logout")
                    return device_keep
                else:
                    #If not, add to ARP
                    tn.write(update_command.encode('ascii') + b"\n")
                    #Update command
                    time.sleep(3)
                    tn.read_until(prompt)
                    time_update = current_time()
                    booking.writerow([time_update,"update"])
                    print(f"{time_update} | Update")
                    #Close telnet connect
                    tn.write("exit".encode('ascii') + b"\n")
                    tn.close()
                    print("Logout")
                    return 404
    #If ConnectionRefusedError
    except ConnectionRefusedError as connect_refuse:
        logging.warning(connect_refuse)
        return True
    except Exception as error_status:
        logging.exception(error_status)
        return False
