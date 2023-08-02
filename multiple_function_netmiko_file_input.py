from os import system
from netmiko import ConnectHandler
from datetime import datetime
import argparse
import config
# from flask import Flask,request


def main():
    """This fuction takes user decision
    Whether user want to execute manual config or predefined config"""
    # Below will get the required details and connects to device.
    system("cls")
    get_device_details()
    # Below code will take input from user
    # whether user want to run Predefined commands or run manual commands
    while True:
        try:
            system("cls")
            predefined_manual_config = int(
                input(
                    """\nPlease choose from following actions.
                    1. Predefined commands
                    2. Enter commands manually and execute
                    Enter number 1 or 2 """
                )
            )
            
            break
        except ValueError:
            print("Please enter number 1 or 2:")
    match predefined_manual_config:
        case 1:
            # This function is used to execute predefined config
            predefined_config()
        case 2:
            # This function is used to execute any manual config which user gives
            manual_config()

device_list=[]
def get_device_details():
    """Function takes required arguments for netmiko
    establish ssh connection. Stores in dictionary router.""" 
    parser=argparse.ArgumentParser(description="This program takes input of file name")
    parser.add_argument("--file_name",help="Enter file name",default="device_details1.csv")
    args=parser.parse_args()
    with open(args.file_name,"r") as file:
            reader = file
            print(reader)
            for ip in reader:
                individual_deivice_dict={"ip":ip.strip(),
                                        "device_type":config.DEVICE_TYPE,
                                        "username":config.USERNAME,
                                        "password":config.PASSWORD,
                                        }
                device_list.append(individual_deivice_dict)
    for each_device in device_list:
            ConnectHandler(**each_device)


def command_executor(device_name,commands,final_show_decision):
    """function is used to ssh into devie.
    Execute config either predefined or manually entered by users"""
    system("cls")
    ssh=(ConnectHandler(**device_name))
    # below is to execute commands in global configuration mode
    if final_show_decision == 1:
        now=datetime.now()
        print(f"\nConnection established\n device= {device_name}")
        with open(f"{device_name['ip']}{now.strftime('_%m_%d_%Y_%H_%M_%S')}.csv","a") as file:
            file.write(f"\nConnection established\n device= {device_name}")
            print("\n", commands)
            result = ssh.send_config_set(commands)
            file.write(f"\n{result}\n")
            print("Commands executed")
    else:
        i=0
        now=datetime.now()
        file=open(f"{device_name['ip']}{now.strftime('_%m_%d_%Y_%H_%M_%S')}.csv","a")
        print(f"\nConnection established\n device= {device_name}")
        file.write(f"\nConnection established\n device= {device_name}")
        for each_command in commands:
            result = ssh.send_command(each_command,read_timeout=100)
            file.write(f"\n{each_command}")
            file.write(f"\n{result}\n")
        file.close()
        print("Commands executed")


def manual_config():
    """function takes manual config from user and store it in list
    and forward to command executor at end"""
    system("cls")
    """Below code will take input from user 
    whether user want to run show commands or configurational changes"""
    while True:
        system("cls")
        try:
            manual_show_desicion = int(
                input(
                    """\nPlease choose from following actions.\n 
                    1. Commands for global config \n 
                    2. Show commands\n\nEnter number 1 or 2 """
                )
            )
            break
        except ValueError:
            print("Please enter number 1 or 2:")
    while True:
        system("cls")
        try:
            Same_commands = int(
                input(
                    """\nPlease choose from following actions.\n 
                    1. Same commands on all devices \n 
                    2. Different command on each device\nEnter 1 or 2 """
                )
            )
            break
        except ValueError:
            print("Please enter number 1 or 2:")  
    system("cls")
    print(
        """\n\nPlease enter list of the commands need to be executed 
        or hit enter after entering each command
        \n-----Enter 'Finish' to finish and execute---\n"""
    )
    # below is loop to create list of commands
    if Same_commands==1:
        if manual_show_desicion == 1:
            manual_commands=[]
            while True:
                user_input = str(input("(config)# "))
                if user_input.title() != "Finish":
                    manual_commands.append(user_input)
                else:
                    break
        else:
            manual_commands=[]
            while True:
                user_input = str(input("Previlige_mode>>> "))
                if user_input.title() != "Finish":
                        manual_commands.append(user_input)
                else:
                    break
        for each_device in device_list:
            command_executor(each_device,manual_commands, manual_show_desicion)       
    else:
        for each_device in device_list:
            system("cls")
            print(f"Enter config for \n{each_device}")
            if manual_show_desicion == 1:
                manual_commands=[]
                while True:
                    user_input = str(input("(config)# "))
                    if user_input.title() != "Finish":
                        manual_commands.append(user_input)
                    else:
                        break
            else:
                manual_commands=[]
                while True:
                    user_input = str(input("Previlige_mode>>> "))
                    if user_input.title() != "Finish":
                        manual_commands.append(user_input)
                    else:
                        break
            command_executor(each_device,manual_commands, manual_show_desicion)


def predefined_config():
    """Below function list the available predefined configuration.
    Accourding to user input it will call the function which can execute user requirement
    """
    system("cls")
    print(
        """\nPlease choose from following configs.
        Each config has its own configuration and show commands
        1. loopback config--> Supported
        2. Routing protocal config(EIGRP,RIP,OSPF)--> Only static supported
        3. Show run from input devices--> supported
    """
    )
    config_choice = int(input(">>> "))
    match config_choice:
        case 1:
            # configuring loopback
            loopback_congfig()
        case 2:
            # Below can configure routing protocal but not created at
            routing_protocal_config()
        case 3:
            # Below can configure ACL protocal but not created at
            show_run()

loopback_commands_list=[]
def loopback_congfig():
    """function create loopback and asks for printing configuration"""
    system("cls")
    for each_device in device_list:
        print(f"\n{each_device}")
        number_of_interfaces = int(input("\nEnter how many interfaces you want to create: "))
        for _ in range(number_of_interfaces):
            print(f"\n{each_device}")
            interface_name = input("\nEnter loopback interface name: ")
            interface_ip = input("Enter interface IP: ")
            subnet_mask = input("Enter subnet mask: ")
            description = input("Enter description: ")
            loopback_commands = [
                "interface " + interface_name,
                "ip address " + interface_ip + " " + subnet_mask,
                "description " + description,
            ]
            command_executor(each_device,loopback_commands, final_show_decision=1)
        # Below show commands defined
    show_commands = input(
        "\nDo you want to check the show commands (enter yes or no to proceed): "
    )
    if show_commands.lower() == "yes":
        global global_show_desicion
        global_show_desicion = 0
        loopback_show_command_list = [
            "sh ip int bri",
            f"sh int {interface_name}",
            f"sh run int {interface_name}",
        ]
    for each_device in device_list:
        command_executor(each_device,
            loopback_show_command_list, final_show_decision=0
        )  # calling command executor to execute show commands


def routing_protocal_config():
    while True:
        try:
            system("cls")
            routing_protocal_choise=int(input("""Choose from below:
                                              1. Static routing-->Supported
                                              2. RIP
                                              3. EIGRP
                                              4. OSPF
                                              5. BGP
                                              Enter below: """))
            break
        except ValueError:
            print("Please enter number:")
    match routing_protocal_choise:
        case 1:
            configure_static_routing()
        case 2:
            configure_rip()
        case 3:
            configure_eigrp()
        case 4:
            configutre_ospf()
        case 5:
            configure_bgp()

static_route_command_list=[]
def configure_static_routing():
    static_route_command_list=[]
    system("cls")
    for each_device in device_list:
        print(f"""Please enter below details to create static routes on
              {each_device}""")
        multiple_networks=0
        while True:
            nw_ID=input("Please enter network ID: ")
            mask=input("Please enter subnet mask: ")
            next_hop=input("Please enter next_hop IP: ")
            each_static_route=f"ip route {nw_ID} {mask} {next_hop}"
            static_route_command_list.append(each_static_route)
            try:
                next_static_route= str(input('Do you want to configure another static route enter "yes" or "no"'))
                if next_static_route.lower()=="yes":
                    multiple_networks=1
                elif next_static_route.lower()=="no":
                    break
            except ValueError:
                next_static_route= input('Do you want to configure another static route enter "yes" or "no"')
        if int(multiple_networks) == 1:
            print(static_route_command_list)
            command_executor(each_device,static_route_command_list,final_show_decision=1)
        elif int(multiple_networks) == 0:
            print(each_static_route)
            command_executor(each_device,each_static_route,final_show_decision=1)
    for each_device in device_list:
        show_commands_choise= input("Do you want to run show commands Yes and no: ")
        if show_commands_choise.lower()=="yes":
            show_commands_list=[
                "sh run | in ip route",
                "sh ip route"
                ]
            command_executor(each_device,show_commands_list,final_show_decision=0)
        
    

def configure_rip():
    for each_device in device_list:
        commands=["router rip","version 2"]
        while True:
            network_id= input("Enter network ID: ")
            next_network_id=input("Do you want to enter another network ID yes or no: ")
            if next_network_id == "yes":
                commands.append(f"network {network_id}")
                multiple_network=1
            else:
                break
        if multiple_network==1:
            command_executor(each_device,commands,final_show_decision=1)
        else:
            commands.append(f"network {network_id}")
            command_executor(each_device,commands,final_show_decision=1)
        
            

def configure_eigrp():
    pass

def configutre_ospf():
    pass

def configure_bgp():
    pass


def show_run():
    """This function run show run in all devices"""
    for each_device in device_list:
        print(each_device)
        command_executor(each_device,commands=["show run"],final_show_decision=2)


if __name__ == "__main__":
    main()