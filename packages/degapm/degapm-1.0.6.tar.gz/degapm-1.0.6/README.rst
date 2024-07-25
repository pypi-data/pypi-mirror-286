Package: degapm
================

Module Introduction
--------------------
This module is designed for A2000 test platform backplane control, which includes  
- Get target slot device's voltage and current
- Set target slot device's voltage
- Set slot Pass/Fail LED status  


Function Definition
--------------------
1. get_voltage_current
    - Parameter: 
        - tray: int, specify the device number (0~11)
    - Return:
        - Success: return a tuple (voltage, current)
        - Fail: return false

2. set_voltage
    - Parameter: 
        - tray: int, specify the device number (0~11)
        - value: int, specify the voltage to set_led_status
    - Return:
        - Success: return True
        - Fail: return false

3. set_led_status
    - Parameter: 
        - tray: int, specify the device number (0~11)
        - value: int, specify the status code of LED (0: off; 1: red; 2:green; 3: yellow)
    - Return:
        - Success: return True
        - Fail: return false


Sample Code
--------------
1. get_voltage_current  

::

    # python
    from degapm import degapm

    tray_number = 1
    result = degapm.get_voltage_current(tray_number)
    if result:
        voltage, current = result
        print("device {0} voltage: {1}, current: {2}").format(tray_number, voltage, current)
    else:
    print("Get device {0} voltage & current fail!").format(tray_number)  

2. set_voltage

::

    # python
    from degapm import degapm

    tray_number = 1
    voltage_value = 12000
    if degapm.set_voltage(tray_number, voltage_value):
        print("Set device {0} voltage to {1}").format(tray_number, voltage_value)
    else:
        print("Set device {0} voltage fail!").format(tray_number)  

3. set_led_status

::

    # python
    from degapm import degapm
    
    tray_number = 1
    led_value = 1
    if degapm.set_led_status (tray_number, led_value):
        print("Set device {0} led status to {1}").format(tray_number, led_value)
    else:
        print("Set device {0} led status fail!").format(tray_number)


Contact us
-----------------------------------------------------------------------------------
1. Official website: <https://degastorage.com/>
2. Author E-mail: <jiaming.shi@degastorage.com>





