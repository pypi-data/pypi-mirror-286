#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket  
import sys,json   
import time       

SOCKET_PORT = 6688
CELL_LIST = [0, 1, 2]
TRAY_LIST = [0, 1, 2, 3]
LED_CRTL_LIST = [0, 1, 2, 3]
CMD_LIST = [ "SETV", "GETVC", "LedControl"]
SLOT_DIC = {
    '0': [0, 0] ,
    '1': [0, 1] ,
    '2': [0, 2] ,
    '3': [0, 3] ,
    '4': [1, 0] ,
    '5': [1, 1] ,
    '6': [1, 2] ,
    '7': [1, 3] ,
    '8': [2, 0] ,
    '9': [2, 1] ,
    '10': [2, 2] ,
    '11': [2, 3] ,
}

##################################################################################################
# Set Voltage Message
def setv_req_generate(cell, tray, vol):
    if cell in CELL_LIST:
        if tray in TRAY_LIST:
            cmd = {'cmd':"SETV", 'cell': cell, 'tray': tray, 'vol': vol}
            msg = json.dumps(cmd)
            return msg
        else:
            print("error cell number:{0}".format(cell))
            exit(-1)
    else:
        print("error tray number:{0}".format(tray))
        exit(-1)


# Get Voltage Current Message
def getvc_req_generate(cell, tray):
    if cell in CELL_LIST:
        if tray in TRAY_LIST:
            cmd = {'cmd': "GETVC",'cell': cell, 'tray': tray}
            msg = json.dumps(cmd)
            return msg
        else:
            print("error cell number:{0}".format(cell))
            exit(-1)
    else:
        print("error tray number:{0}".format(tray))
        exit(-1)


# LED Control Message
def ledctrl_req_generate(cell, tray, opt):
    if cell in CELL_LIST:
        if tray in TRAY_LIST:
            if opt in LED_CRTL_LIST:
                cmd = {'cmd': "LedControl", 'cell': cell, 'tray':tray, 'led': opt}
                msg = json.dumps(cmd)
                return msg
            else:
                print("error led cmd:{0}".format(cell))
                exit(-1)
        else:
            print("error cell number:{0}".format(cell))
            exit(-1)
    else:
        print("error tray number:{0}".format(tray))
        exit(-1)

##################################################################################################

# Socket Init
def socket_init():
    try:   
        socket.setdefaulttimeout(10)
        s = socket.socket()         
        host = socket.gethostname() 
        port =  SOCKET_PORT
        s.connect((host, port))   
        return s
    except Exception as e:
        print(e)


# Socket Close
def socket_close(s):
    try:  
        s.close()
    except Exception as e:
        print(e)


# Socket communication
def send_socket_msg(socket, msg):
    try:
        # print(msg)
        socket.settimeout(10)
        socket.send(msg.encode('utf-8'))
        socket.send("\n".encode('utf-8'))
        msg = socket.recv(1024*5)
        msg = msg.decode('utf-8')
        recvmsg = json.loads(msg)
        return recvmsg
    except Exception as e:
        print(e)

##################################################################################################

##################################################################################################

# Transfer cell tray
def slot_transfer(slot):
    cell= SLOT_DIC[str(slot)][0]
    tray = SLOT_DIC[str(slot)][1]
    # print("{0} {1}".format(cell, tray))
    return cell, tray


# set Voltage API
def set_voltage(slot, vol):
    cell, tray = slot_transfer(slot)
    socket = socket_init()
    msg = setv_req_generate(cell, tray, vol)
    recvmsg = send_socket_msg(socket, msg)
    if recvmsg['result'] == "SUCCESS":
        socket_close(socket)
        return True
    elif recvmsg['result'] == "ERROR":
        socket_close(socket)
        return False
    else:
        socket_close(socket)
        return False
    

# get Voltage Current API
def get_voltage_current(slot):
    cell, tray = slot_transfer(slot)
    socket = socket_init()
    msg = getvc_req_generate(cell, tray)
    recvmsg = send_socket_msg(socket, msg)
    if recvmsg['result'] == "SUCCESS":
        vol = recvmsg['vol']
        cur = recvmsg['cur']
        ret_tuple = (vol, cur)
        # print(ret_tuple)
        socket_close(socket)
        return ret_tuple
    elif recvmsg['result'] == "ERROR":
        socket_close(socket)
        return False
    else:
        socket_close(socket)
        return False
    

# set LED API
def set_led_status(slot, opt):
    cell, tray = slot_transfer(slot)
    socket = socket_init()
    msg = ledctrl_req_generate(cell, tray, opt)
    recvmsg = send_socket_msg(socket, msg)
    if recvmsg['result'] == "SUCCESS":
        socket_close(socket)
        return True
    elif recvmsg['result'] == "ERROR":
        socket_close(socket)
        return False
    else:
        socket_close(socket)
        return False