from netmiko import ConnectHandler
import os
import yaml
from audit.functions import device_directories

input_f = open('input.yml', 'r')
input_s = input_f.read()
input_f.close()
input = yaml.load(input_s, Loader=yaml.FullLoader)

devices = input['devices']
output_directory = input['output_directory'] 
username = input['username']
password = input['password']
text_cmds = input['text_cmds']
json_cmds = input['json_cmds'] 
text_and_json_cmds = input['text_and_json_cmds']

for device in devices:
    # Create directories to save the commands output
    directories = device_directories(device, output_directory)
    device_directory = directories[0]
    eos_commands_directory = directories[1]
    json_directory = directories[2]
    text_directory = directories[3]
    # collect show commands
    print("opening connection to " + device)
    switch = {'device_type': 'arista_eos', 'host': device, 'username': username, 'password': password, 'port': '22', 'timeout': 180}
    connection = ConnectHandler(**switch)
    print("collecting show commands on device " + device)
    # collect text commands
    if text_cmds is not None: 
        for cmd in text_cmds: 
            print("collecting " + cmd)
            cmd_output = connection.send_command(cmd)
            f=open(text_directory + "/" + cmd + ".txt", "w")
            f.write(cmd_output)
            f.closed
    if (text_and_json_cmds is not None) and (text_cmds is not None) : 
        for cmd in text_and_json_cmds: 
            if cmd not in text_cmds: 
                print("collecting " + cmd)
                cmd_output = connection.send_command(cmd)
                f=open(text_directory + "/" + cmd + ".txt", "w")
                f.write(cmd_output)
                f.closed
    elif (text_and_json_cmds is not None) and (text_cmds is None):
        for cmd in text_and_json_cmds: 
            print("collecting " + cmd)
            cmd_output = connection.send_command(cmd)
            f=open(text_directory + "/" + cmd + ".txt", "w")
            f.write(cmd_output)
            f.closed
    # collect json commands
    if json_cmds is not None: 
        for cmd in json_cmds: 
            print("collecting " + cmd + "| json")
            cmd_output = connection.send_command(cmd + "| json")
            f=open(json_directory + "/" + cmd + ".json", "w")
            f.write(cmd_output)
            f.closed
    if (text_and_json_cmds is not None) and (json_cmds is not None) : 
        for cmd in text_and_json_cmds: 
            if cmd not in json_cmds: 
                print("collecting " + cmd + "| json")
                cmd_output = connection.send_command(cmd + "| json")
                f=open(json_directory + "/" + cmd + ".json", "w")
                f.write(cmd_output)
                f.closed
    elif (text_and_json_cmds is not None) and (json_cmds is None):
        for cmd in text_and_json_cmds: 
            print("collecting " + cmd + "| json")
            cmd_output = connection.send_command(cmd + "| json")
            f=open(json_directory + "/" + cmd + ".json", "w")
            f.write(cmd_output)
            f.closed
    print("closing connection to " + device)
    connection.disconnect()


