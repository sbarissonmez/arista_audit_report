import yaml 
from audit.functions import str_to_function, generate_main_report, generate_failures_only_report, assemble_main_reports, assemble_failures_only_reports 

input_f = open('input.yml', 'r')
input_s = input_f.read()
input_f.close()
input = yaml.load(input_s, Loader=yaml.FullLoader)

devices = input['devices']
root_dir = input['output_directory'] 
audit_str_list = input['audit']

audit_func_list = str_to_function (audit_str_list)

for device in devices:
    generate_main_report(device, audit_func_list, root_dir)
    generate_failures_only_report(device, audit_func_list, root_dir)

assemble_main_reports(devices, audit_func_list, root_dir)
assemble_failures_only_reports(devices, audit_func_list, root_dir)
