import os
import yaml
from audit.functions import device_directories

input_f = open('input.yml', 'r')
input_s = input_f.read()
input_f.close()
input = yaml.load(input_s, Loader=yaml.FullLoader)

devices = input['devices']
output_directory = input['output_directory'] 
custom_show_tech_support = input['custom_show_tech_support']


# assemble some of the collected txt files into one large file
for device in devices: 
    directories = device_directories(device, output_directory)
    device_directory = directories[0]
    eos_commands_directory = directories[1]
    text_directory = directories[3]
    outfile = open(text_directory + "/custom show tech-support.txt", "w")   
    for item in custom_show_tech_support: 
        infile = open(text_directory + "/" + item + ".txt", "r")
        outfile.write('-'*13 + ' ' + item + ' ' + '-'*13 + '\n'*2)
        for line in infile:  
            outfile.write(line)
        outfile.write('\n'*2)
        infile.close()
    outfile.close()
