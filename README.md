## Arista Audit Report

This repo has python content to collect eos commands from Arista devices. It also has python content to audit offline the data collected and to generate a report.

### Requirements

```
python -V
Python 3.7.7
```

```
pip freeze | grep netmiko
netmiko==3.1.1
```

### How to use this repository 

Install the requirements described in the above section.  

Then update the file [input.yml](input.yml). It has the required input for the various scripts available in this repository.   

Then you can run the script [collect_eos_commands.py](collect_eos_commands.py) to collect commands output from EOS devices.  

If you want to generate offline a custom show tech-support text file, run the script [custom_show_tech_support.py](custom_show_tech_support.py).  

Once you collected the commands output, you can run the script [generate_audit_report.py](generate_audit_report.py) to generate reports.  

