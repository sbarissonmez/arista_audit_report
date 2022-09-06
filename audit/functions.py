import datetime
import os
import json

def device_directories (device, root_dir):
    """Create directories for the device

    Create the directories root_dir/device, root_dirdevice/eos_commands, root_dir/device/eos_commands/json, root_dir/device/eos_commands/text, root_dir/device/reports, root_dir/device/reports/main, root_dir/device/reports/failures_only. 

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        name of the the directories for the device. 
    """ 
    cwd = os.getcwd()
    output_directory = os.path.dirname(cwd + "/" + root_dir + "/")
    device_directory = output_directory + '/' + device
    eos_commands_directory = device_directory + '/' + "eos_commands"
    json_directory = eos_commands_directory + '/' + "json"    
    text_directory = eos_commands_directory + '/' + "text"  
    reports_directory = device_directory + '/' + "reports"
    main_reports_directory = reports_directory + '/' + "main"
    failures_only_reports_directory = reports_directory + '/' + "failures_only"
    for directory in [output_directory, device_directory, eos_commands_directory, json_directory, text_directory, reports_directory, main_reports_directory, failures_only_reports_directory]: 
        if not os.path.exists(directory):
            os.makedirs(directory)
    result = device_directory, eos_commands_directory, json_directory, text_directory, reports_directory, main_reports_directory, failures_only_reports_directory
    return result

def str_to_function (audit_str_list):
    """map a list of string into a list of functions 

    Parameters
    ----------
    audit_str_list : list
        list of string

    Returns
    -------
    list
        list of functions
    """
    map = {'print_hostname': print_hostname, 'print_version': print_version, 'check_inventory': check_inventory, 'check_power': check_power, 'check_cooling': check_cooling, 'check_temperature': check_temperature, 'check_temperature_transceivers': check_temperature_transceivers, 'check_reload_cause_history': check_reload_cause_history, 'check_reload_cause_full': check_reload_cause_full, 'print_lldp': print_lldp, 'check_bgp': check_bgp, 'check_mlag': check_mlag} 
    audit_func_list = []
    for item in audit_str_list : 
        audit_func_list.append(map[item])
    return audit_func_list


def init (device, root_dir):
    """Generates files with the device IP address or hostname.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        name of the two generated files. 
    """
    directories = device_directories(device, root_dir)
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    main_report = open(main_reports_directory + '/init.txt', 'w') 
    failures_only_report = open(failures_only_reports_directory + '/init.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write ('-'*13 + ' Report for device ' + device + ' ' + '-'*13 + "\n"*2)
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def print_hostname (device, root_dir):
    """Generates files with the device hostname and fqdn.

    Required EOS command: show hostname | json

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        name of the two generated files. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show hostname"
    main_report = open(main_reports_directory + '/print_hostname.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/print_hostname.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Device hostname " + '*'*10 + "\n"*2)
        item.write('Description: include the device hostname and fqdn\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: This is a report without any test so there is no failure/passing condition\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    hostname = data_json['hostname']
    fqdn = data_json['fqdn']
    for item in [main_report, failures_only_report]:
        item.write('Hostname: ' + hostname + '\n')
        item.write('FQDN: ' + fqdn + '\n')
        item.write('\n')
        item.close() 
    result = main_report.name, failures_only_report.name
    return result

def print_version (device, root_dir):
    """Generates files with some details regarding the device (HW model, SN, SW release, uptime).

    Required EOS command: show version | json

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        name of the two generated files. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show version"
    main_report = open(main_reports_directory + '/print_version.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/print_version.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Device details " + '*'*10 + "\n"*2)
        item.write('Description: include some details regarding the device (HW model, SN, SW release, uptime)\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: This is a report without any test so there is no failure/passing condition\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    modelName = data_json['modelName']
    version = data_json['version']
    uptime_seconds = data_json["uptime"]
    uptime = str(datetime.timedelta(seconds = int(uptime_seconds))) 
    serialNumber = data_json["serialNumber"]
    for item in [main_report, failures_only_report]:
        item.write('Model: ' + modelName + '\n')
        item.write('Serial number: ' + serialNumber + '\n')
        item.write('Version: ' + version + '\n')
        item.write('Uptime: ' + uptime + '\n')
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_inventory (device, root_dir):
    """Check the hardware inventory and generates files with the tests result.

    Required EOS command: show version | json
    Test failure conditions: A transceiver test fails if its manufacturer is neither "Arista Networks" nor "Arastra, Inc". A power supply test fails if a power supply slot has no power supply unit inserted. 

    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file.  
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show inventory"
    main_report = open(main_reports_directory + '/check_inventory.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_inventory.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Device inventory " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the hardware inventory\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write('Test failure conditions: A test fails if the manufacturer of a transceiver is neither "Arista Networks" nor "Arastra, Inc", or if a power supply slot has no power supply unit inserted\n\n')
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    description = data_json['systemInformation']['description']
    for item in [main_report, failures_only_report]:
        item.write('Device description: ' + description + '\n')
        item.write('\n')
    for item in [main_report, failures_only_report]:
        item.write('Power Supplies: \n')
    at_least_one_test_in_the_loop_failed = False
    for ps in data_json['powerSupplySlots']: 
        slot = str(ps)
        name = data_json['powerSupplySlots'][ps]['name']
        serialNum = data_json['powerSupplySlots'][ps]['serialNum']
        if name == 'Not Inserted': 
            result = 'FAIL'
            at_least_one_test_in_the_loop_failed = True
        else:
            result = 'PASS'
        message = 'Slot: ' + slot + ' *** Model: ' + name + ' *** SN: ' + serialNum + ' *** Result: ' + result + '\n'
        main_report.write(message)
        if result == 'FAIL':
            failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.write('Fan modules: \n')
    for fan_module in data_json['fanTraySlots']: 
        slot = str(fan_module)
        name = data_json['fanTraySlots'][fan_module]['name']
        main_report.write('Module: ' + slot + ' *** Model: ' + name + '\n')
    failures_only_report.write("The script doesnt run tests about the Fans modules ...\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.write('Transceivers: \n')
    at_least_one_test_in_the_loop_failed = False
    for transceiver in sorted(data_json["xcvrSlots"]):
        transceiver = str(transceiver)
        mfgName = data_json['xcvrSlots'][transceiver]['mfgName']
        serialNum = data_json['xcvrSlots'][transceiver]['serialNum']
        modelName = data_json['xcvrSlots'][transceiver]['modelName']
        if (mfgName == 'Arista Networks') or (mfgName == 'Arastra, Inc'):
            result = 'PASS'
        elif mfgName == 'Not Present': 
            result = 'PASS'
        else:
            result = 'FAIL'
            at_least_one_test_in_the_loop_failed = True
        if mfgName != "Not Present": 
            message = "Port: " + transceiver + ' *** Manufacturer: ' + mfgName + ' *** Model: ' + modelName + ' *** SN: ' + serialNum + ' *** Result: ' + result + "\n"
            main_report.write(message)
            if result == 'FAIL':
                failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_power (device, root_dir):
    """Check the power status and generates files with the tests result.

    Required EOS command: show system environment power | json
    Test failure conditions: A test fails if the status of a power supply is not ok. 

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file.  
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show system environment power"
    main_report = open(main_reports_directory + '/check_power.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_power.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Power supplies status " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the power status\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: A test fails if the status of a power supply is not ok\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    at_least_one_test_in_the_loop_failed = False
    for powersupply in data_json['powerSupplies']:
        state = data_json['powerSupplies'][powersupply]['state']
        if state == 'ok': 
            result = 'PASS'
        else:
            result = 'FAIL'
            at_least_one_test_in_the_loop_failed = True
        message = "Power supply: " + powersupply + ' *** Status: ' + state + ' *** Result: ' + result + "\n"
        main_report.write(message)
        if result == 'FAIL':
            failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_cooling (device, root_dir):
    """Check the cooling status and generates files with the tests result.

    Required EOS command: show system environment cooling | json
    Test failure conditions: A test fails if the status of a fan is not ok.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show system environment cooling"
    main_report = open(main_reports_directory + '/check_cooling.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_cooling.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Cooling status " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the cooling status\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: A test fails if the status of a fan is not ok\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    for item in [main_report, failures_only_report]:
        item.write('Power supplies: \n')
    at_least_one_test_in_the_loop_failed = False
    for ps in data_json['powerSupplySlots']:
        for fan in ps['fans']: 
            status = fan['status'] 
            label = fan['label']
            if status == 'ok': 
                result = 'PASS'
            else:
                result = 'FAIL'
                at_least_one_test_in_the_loop_failed = True
            message = "Fan: " + label + ' *** Status: ' + status + ' *** Result: ' + result + "\n"
            main_report.write(message)
            if result == 'FAIL':
                failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\nFan modules: \n')
    at_least_one_test_in_the_loop_failed = False
    for fantrayslot in data_json['fanTraySlots']:
        for fan in fantrayslot['fans']: 
            status = fan['status'] 
            label = fan['label']
            if status == 'ok': 
                result = 'PASS'
            else:
                result = 'FAIL'
                at_least_one_test_in_the_loop_failed = True
            message = "Fan: " + label + ' *** Status: ' + status + ' *** Result: ' + result + "\n"
            main_report.write(message)
            if result == 'FAIL':
                failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_temperature (device, root_dir):
    """Check the temperature status and generates files with the tests result.

    Required EOS command: show system environment temperature | json
    Test failure conditions: A sensor test fails if a sensor HW status is not OK or if a sensor alert count is > 0 or if a sensor is currently in alert state. The system temperature test fails if the system status is not OK.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show system environment temperature"
    main_report = open(main_reports_directory + '/check_temperature.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_temperature.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Temperature status " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the temperature status\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: A test fails if a sensor HW status is not OK or if a sensor alert count is > 0 or if a sensor is currently in alert state. The system temperature test fails if the system status is not OK\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    systemStatus = json.loads(data)['systemStatus']
    if systemStatus != 'temperatureOk': 
        result = 'FAIL'
    else:
        result = 'PASS'
        systemStatus = 'ok'
    for item in [main_report, failures_only_report]:
        item.write("System temperature: \n") 
    message = "Status: " + systemStatus + ' *** Result: ' + result + '\n'
    main_report.write(message)
    if result == 'FAIL': 
        failures_only_report.write(message)
    if result == 'PASS': 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write("\nSensors: \n" ) 
    at_least_one_test_in_the_loop_failed = False
    for sensor in data_json["tempSensors"]:
        hwStatus = sensor['hwStatus']
        alertCount = sensor['alertCount']
        description = sensor['description']
        name = sensor['name']
        maxTemperature = sensor['maxTemperature']
        inAlertState = sensor['inAlertState']
        maxTemperatureLastChange_epoch = sensor['maxTemperatureLastChange']
        maxTemperatureLastChange = datetime.datetime.fromtimestamp(maxTemperatureLastChange_epoch).strftime("%d %b %Y %H:%M:%S")
        if hwStatus != 'ok' or alertCount!= 0 or str(inAlertState) != "False": 
            result = 'FAIL'
            at_least_one_test_in_the_loop_failed = True
        else:
            result = 'PASS'
        message = "Sensor: " + name + ' *** Description: ' + description + ' *** HW status: ' + hwStatus + ' *** Alert count: ' + str(alertCount) + ' *** In alert state: ' + str(inAlertState) + ' *** Max temperature (C): ' + str(int(maxTemperature)) + ' *** Max temperature last change: ' + maxTemperatureLastChange + ' *** Result: ' + result + "\n"
        main_report.write(message)
        if result == 'FAIL':
            failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write("\nCard Slot: \n" ) 
    at_least_one_test_in_the_loop_failed = False
    for card in data_json["cardSlots"]: 
        entPhysicalClass = card['entPhysicalClass']
        relPos = card['relPos']
        for sensor in card["tempSensors"]: 
            hwStatus = sensor['hwStatus']
            alertCount = sensor['alertCount']
            description = sensor['description']
            name = sensor['name']
            maxTemperature = sensor['maxTemperature']
            inAlertState = sensor['inAlertState']
            maxTemperatureLastChange_epoch = sensor['maxTemperatureLastChange']
            maxTemperatureLastChange = datetime.datetime.fromtimestamp(maxTemperatureLastChange_epoch).strftime("%d %b %Y %H:%M:%S")
            if hwStatus != 'ok' or alertCount!= 0 or str(inAlertState) != "False": 
                result = 'FAIL'
                at_least_one_test_in_the_loop_failed = True
            else:
                result = 'PASS'
            message = "Sensor: " + name + ' *** Description: ' + description + ' *** Card type: ' + entPhysicalClass + ' *** Card position: ' + relPos + ' *** HW status: ' + hwStatus + ' *** Alert count: ' + str(alertCount) + ' *** In alert state: ' + str(inAlertState) + ' *** Max temperature (C): ' + str(int(maxTemperature)) + ' *** Max temperature last change: ' + maxTemperatureLastChange + ' *** Result: ' + result + "\n"
            main_report.write(message)
            if result == 'FAIL':
                failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.write("Power Supplies: \n" ) 
    at_least_one_test_in_the_loop_failed = False
    for item in data_json["powerSupplySlots"]: 
        for sensor in item["tempSensors"]: 
            hwStatus = sensor['hwStatus']
            alertCount = sensor['alertCount']
            description = sensor['description']
            name = sensor['name']
            maxTemperature = sensor['maxTemperature']
            inAlertState = sensor['inAlertState']
            maxTemperatureLastChange_epoch = sensor['maxTemperatureLastChange']
            maxTemperatureLastChange = datetime.datetime.fromtimestamp(maxTemperatureLastChange_epoch).strftime("%d %b %Y %H:%M:%S")
            if hwStatus != 'ok' or alertCount!= 0 or str(inAlertState) != "False": 
                result = 'FAIL'
                at_least_one_test_in_the_loop_failed = True
            else:
                result = 'PASS'
            message = "Sensor: " + name + ' *** Description: ' + description + ' *** HW status: ' + hwStatus + ' *** Alert count: ' + str(alertCount) + ' *** In alert state: ' + str(inAlertState) + ' *** Max temperature (C): ' + str(int(maxTemperature)) + ' *** Max temperature last change: ' + maxTemperatureLastChange + ' *** Result: ' + result + "\n"
            main_report.write(message)
            if result == 'FAIL':
                failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_temperature_transceivers (device, root_dir):
    """Check the transceivers temperature status and generates files with the tests result.

    Required EOS command: show system environment temperature transceiver | json
    Test failure conditions: A test fails if a sensor HW status is not OK or if a sensor alert count is > 0 or if a sensor is currently in alert state.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.
    
    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show system environment temperature transceiver"
    main_report = open(main_reports_directory + '/check_temperature_transceivers.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_temperature_transceivers.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " transceivers temperature status " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the transceivers temperature status\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: A test fails if a sensor HW status is not OK or if a sensor alert count is > 0 or if a sensor is currently in alert state\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    at_least_one_test_in_the_loop_failed = False
    for sensor in data_json["tempSensors"]:
        hwStatus = sensor['hwStatus']
        alertCount = sensor['alertCount']
        description = sensor['description']
        maxTemperature = sensor['maxTemperature']
        inAlertState = sensor['inAlertState']
        maxTemperatureLastChange_epoch = sensor['maxTemperatureLastChange']
        maxTemperatureLastChange = datetime.datetime.fromtimestamp(maxTemperatureLastChange_epoch).strftime("%d %b %Y %H:%M:%S")
        if hwStatus != 'ok' or alertCount!= 0 or str(inAlertState) != "False": 
            result = 'FAIL'
            at_least_one_test_in_the_loop_failed = True
        else:
            result = 'PASS'
        message = 'Description: ' + description + ' *** HW status: ' + hwStatus + ' *** Alert count: ' + str(alertCount) + ' *** In alert state: ' + str(inAlertState) + ' *** Max temperature (C): ' + str(int(maxTemperature)) + ' *** Max temperature last change: ' + maxTemperatureLastChange + ' *** Result: ' + result + "\n"
        main_report.write(message)
        if result == 'FAIL':
            failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    at_least_one_test_in_the_loop_failed = False
    for card in data_json["cardSlots"]: 
        if card['entPhysicalClass'] == "Linecard":
            for sensor in card["tempSensors"]: 
                hwStatus = sensor['hwStatus']
                alertCount = sensor['alertCount']
                description = sensor['description']
                maxTemperature = sensor['maxTemperature']
                inAlertState = sensor['inAlertState']
                maxTemperatureLastChange_epoch = sensor['maxTemperatureLastChange']
                maxTemperatureLastChange = datetime.datetime.fromtimestamp(maxTemperatureLastChange_epoch).strftime("%d %b %Y %H:%M:%S")
                if hwStatus != 'ok' or alertCount!= 0 or str(inAlertState) != "False": 
                    result = 'FAIL'
                    at_least_one_test_in_the_loop_failed = True
                else:
                    result = 'PASS'
                message = 'Description: ' + description + ' *** HW status: ' + hwStatus + ' *** Alert count: ' + str(alertCount) + ' *** In alert state: ' + str(inAlertState) + ' *** Max temperature (C): ' + str(int(maxTemperature)) + ' *** Max temperature last change: ' + maxTemperatureLastChange + ' *** Result: ' + result + "\n"
                main_report.write(message)
                if result == 'FAIL':
                    failures_only_report.write(message)
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_reload_cause_history (device, root_dir):
    """Check the cause for the last 10 reload and generates files with the tests result.

    Required EOS command: show reload cause history | json
    Test failure conditions: A test fails if a device reload was not requested by user.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.
    
    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show reload cause history"
    main_report = open(main_reports_directory + '/check_reload_cause_history.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_reload_cause_history.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Reload cause history " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the cause for the last 10 reload\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: A test fails if the device reload was not requested by user\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    at_least_one_test_in_the_loop_failed = False
    for reboot_id in range(0,10):
        reboot_id = str(reboot_id)
        if reboot_id in data_json["resetHistory"]:
            for reboot in data_json["resetHistory"][reboot_id]:
                description = data_json["resetHistory"][reboot_id][reboot][0]['description']
                timestamp_epoch = data_json["resetHistory"][reboot_id][reboot][0]['timestamp']
                timestamp = datetime.datetime.fromtimestamp(timestamp_epoch).strftime("%d %b %Y %H:%M:%S")
                if description != "Reload requested by the user.": 
                    result = "FAIL"
                    at_least_one_test_in_the_loop_failed = True
                else:
                    result = "PASS" 
                message = "Time: " + timestamp  + " *** Reason: " + description + " *** Result: " + result + '\n'
                main_report.write(message)
                if result == 'FAIL':
                    failures_only_report.write(message) 
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_reload_cause_full (device, root_dir):
    """Check the cause for the most recent reload and generates files with the tests result.

    Required EOS command: show reload cause full | json
    Test failure conditions: The test fails if the device reload was not requested by user.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.
    
    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show reload cause full"
    main_report = open(main_reports_directory + '/check_reload_cause_full.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_reload_cause_full.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " Reload cause full " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the cause of the most recent reload\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: The test fails if the device reload was not requested by user\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    at_least_one_test_in_the_loop_failed = False
    for item in data_json["resetCauses"]: 
        description = item['description']
        timestamp_epoch = item['timestamp']
        timestamp = datetime.datetime.fromtimestamp(timestamp_epoch).strftime("%d %b %Y %H:%M:%S")
        if description != "Reload requested by the user.": 
            result = "FAIL"
            at_least_one_test_in_the_loop_failed = True
        else:
            result = "PASS" 
        message = "Time: " + timestamp  + " *** Reason: " + description + " *** Result: " + result + '\n'
        main_report.write(message) 
        if result == 'FAIL':
            failures_only_report.write(message)
    if at_least_one_test_in_the_loop_failed == True: 
        failures_only_report.write("The other tests succesfully passed\n")
    if at_least_one_test_in_the_loop_failed == False: 
        failures_only_report.write("All tests successfully passed\n")
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def print_lldp (device, root_dir):
    """Generates files with the LLDP topology.

    Required EOS command: show lldp neighbors | json

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.
    
    Returns
    -------
    tuple
        name of the two generated files. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show lldp neighbors"
    main_report = open(main_reports_directory + '/print_lldp.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/print_lldp.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " LLDP topology " + '*'*10 + "\n"*2)
        item.write('Description: include the lldp topology\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: This is a report without any test so there is no failure/passing condition\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    for item in data_json['lldpNeighbors']:  
        neighborDevice = item['neighborDevice']
        neighborPort = item['neighborPort']
        port = item['port']
        for f in [main_report, failures_only_report]:
            f.write("Interface: " + port + ' *** LLDP neighbor: ' + neighborDevice + " *** LLDP remote port: " + neighborPort + "\n")
    for f in [main_report, failures_only_report]:
        f.write('\n')
        f.close()
    result = main_report.name, failures_only_report.name
    return result

def check_bgp (device, root_dir):
    """Check BGP status for all configured vrf and generates files with the tests result.

    Required EOS command: show ip bgp summary vrf all | json
    Test failure conditions: A test fails if a BGP session is not established.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show ip bgp summary vrf all"
    main_report = open(main_reports_directory + '/check_bgp.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_bgp.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " BGP sessions state " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the bgp status for all configured vrf\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: A test fails if a BGP session is not established\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    for vrf in data_json['vrfs']: 
        vrf = vrf
        for item in [main_report, failures_only_report]:
            item.write("vrf: " + vrf + "\n") 
        at_least_one_test_in_the_loop_failed = False
        for peer in data_json['vrfs'][vrf]['peers']: 
            peer = peer
            asn = data_json['vrfs'][vrf]['peers'][peer]['asn']
            peerState = data_json['vrfs'][vrf]['peers'][peer]['peerState']
            upDownTime = datetime.datetime.fromtimestamp(data_json['vrfs'][vrf]['peers'][peer]['upDownTime']).strftime("%d %b %Y %H:%M:%S")
            if peerState != 'Established': 
                result = 'FAIL'
                at_least_one_test_in_the_loop_failed = True
            else:
                result = 'PASS'
            message = "Peer: " + peer + " *** ASN: " + asn + " *** State: " + peerState + " *** Up/Down: " + upDownTime + " *** Result: " + result + "\n"
            main_report.write(message)
            if result == 'FAIL':
                failures_only_report.write(message)
        if at_least_one_test_in_the_loop_failed == True: 
            failures_only_report.write("The other tests succesfully passed\n")
        if at_least_one_test_in_the_loop_failed == False: 
            failures_only_report.write("All tests successfully passed\n")
        for item in [main_report, failures_only_report]:
            item.write('\n')
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def check_mlag (device, root_dir):
    """Check MLAG state and generates files with the tests result.

    Required EOS command: show mlag detail | json
    Test failure conditions: The test fails if the MLAG state is active and the negotiation status is not connected.

    Parameters
    ----------
    device : str
        Device IP address or hostname.
    root_dir: str
        Root directory for all the outputs.

    Returns
    -------
    tuple
        The name of the main report file and the name of the failures_only report file. 
    """
    directories = device_directories(device, root_dir)
    json_directory = directories[2]
    main_reports_directory = directories[5]
    failures_only_reports_directory = directories[6]
    command = "show mlag detail"
    main_report = open(main_reports_directory + '/check_mlag.txt', 'w')
    failures_only_report = open(failures_only_reports_directory + '/check_mlag.txt', 'w') 
    for item in [main_report, failures_only_report]:
        item.write('*'*10 + " MLAG state " + '*'*10 + "\n"*2)
        item.write('Description: include tests report about the mlag status\n')
        item.write("Required EOS command: " + command + ' | json\n')
        item.write("Test failure conditions: The test fails if the MLAG state is active and the negotiation status is not connected\n\n")
    f = open(json_directory + '/' + command + '.json', 'r') 
    data = f.read()
    f.close()
    data_json = json.loads(data) 
    state = data_json["state"] 
    if state == "active": 
        negStatus = data_json["negStatus"]
        configSanity = data_json["configSanity"]
        peerAddress = data_json["peerAddress"] 
        if negStatus != 'connected': 
            result = 'FAIL'
        elif negStatus == 'connected':
            result = 'PASS' 
        if result == 'FAIL':
            for item in [main_report, failures_only_report]:    
                item.write("Peer: " + peerAddress + "\n")
                item.write("State: " + state + "\n")
                item.write("Negotiation Status: " + negStatus + "\n")
                item.write("Config Sanity: " + configSanity + "\n")
                item.write("\nTest result: " + result + "\n")  
        elif result == 'PASS': 
            main_report.write("Peer: " + peerAddress + "\n")
            main_report.write("State: " + state + "\n")
            main_report.write("Negotiation Status: " + negStatus + "\n")
            main_report.write("Config Sanity: " + configSanity + "\n")
            main_report.write("\nTest result: " + result + "\n")  
            failures_only_report.write("All tests successfully passed\n")
    elif state == "disabled": 
        for item in [main_report, failures_only_report]:
            item.write("MLAG is " + state +  "\n")  
    for item in [main_report, failures_only_report]:
        item.write('\n')
        item.close()
    result = main_report.name, failures_only_report.name
    return result

def generate_main_report(dev, topic, root_dir): 
    """Generate the main report for a device

    Parameters
    ----------
    dev : str
        Device IP address or hostname.
    topic : list
        The list of functions to use to generate the device report 
    root_dir: str
        Root directory for all the outputs.
    """
    directories = device_directories(dev, root_dir)
    reports_directory = directories[4]
    outfile = open(reports_directory + "/main.txt", "w")
    infile = open(init(dev, root_dir)[0], "r")
    for line in infile:  
        outfile.write(line)
    infile.close()
    for item in topic:
        infile = open(item(dev, root_dir)[0], "r")
        for line in infile:  
            outfile.write(line)
        infile.close()
    outfile.close()

def generate_failures_only_report(dev, topic, root_dir): 
    """Generate the failure_only report for a device

    Parameters
    ----------
    dev : str
        Device IP address or hostname.
    topic : list
        The list of functions to use to generate the device report 
    root_dir: str
        Root directory for all the outputs.
    """
    directories = device_directories(dev, root_dir)
    reports_directory = directories[4]
    outfile = open(reports_directory + "/failures_only.txt", "w")
    infile = open(init(dev, root_dir)[1], "r")
    for line in infile:  
        outfile.write(line)
    infile.close()
    for item in topic:
        infile = open(item(dev, root_dir)[1], "r")
        for line in infile:  
            outfile.write(line)
        infile.close()
    outfile.close()

def assemble_main_reports(devices, topic, root_dir):
    """Assembles the generated main report of each device into one report for all devices

    Parameters
    ----------
    devices : list
        List of devices IP addresses or hostnames. 
    topic : list
        The list of functions to use to generate the device report 
    root_dir: str
        Root directory for all the outputs.
    """    
    audit_str_list = []
    for item in topic: 
        audit_str_list.append(item.__name__)
    network_report = open(root_dir + "/main.txt", "w")
    network_report.write('Report generated using Python the ' + str(datetime.datetime.now().strftime("%d %b %Y at %H:%M:%S")) + "\n"*2)
    network_report.write ('The list of devices audited is: ' + str(devices) + '\n')
    network_report.write ('The list of topics audited is: ' + str(audit_str_list) + '\n'*2)
    network_report.write('The file main.txt shows the details for all the tests.\n')
    network_report.write("The file failures_only.txt shows only the tests that failed." + "\n"*2)
    for device in devices:
        directories = device_directories(device, root_dir)
        reports_directory = directories[4]
        device_report = open(reports_directory + "/main.txt", "r")
        for line in device_report:  
            network_report.write(line)
        device_report.close()

def assemble_failures_only_reports(devices, topic, root_dir): 
    """Assembles the generated failures_only report of each device into one report for all devices

    Parameters
    ----------
    devices : list
        List of devices IP addresses or hostnames. 
    topic : list
        The list of functions to use to generate the device report 
    root_dir: str
        Root directory for all the outputs.

    """ 
    audit_str_list = []
    for item in topic: 
        audit_str_list.append(item.__name__)
    network_report_failures_only = open(root_dir + "/failures_only.txt", "w")
    network_report_failures_only.write('Report generated using Python the ' + str(datetime.datetime.now().strftime("%d %b %Y at %H:%M:%S")) + "\n"*2)
    network_report_failures_only.write ('The list of devices audited is: ' + str(devices) + '\n')
    network_report_failures_only.write ('The list of topics audited is: ' + str(audit_str_list) + '\n'*2)
    network_report_failures_only.write('The file failures_only.txt shows only the tests that failed.\n')
    network_report_failures_only.write("The file main.txt shows the details for all the tests." + "\n"*2)
    for device in devices:
        directories = device_directories(device, root_dir)
        reports_directory = directories[4]
        device_report = open(reports_directory + "/failures_only.txt", "r")
        for line in device_report:  
            network_report_failures_only.write(line)
        device_report.close()


