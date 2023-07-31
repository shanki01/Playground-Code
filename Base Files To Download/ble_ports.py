import time
import bluetooth
import ble_advertising
from hub import *
import device
import force_sensor
import distance_sensor
import motor
import color_sensor

deviceTypeLookup = {48: 'motor', 49: 'big motor', 61: 'color', 62: 'dist', 63: 'force', 255: 'none'}
hubPorts = {'A': 'N', 'B': 'N', 'C': 'N', 'D': 'N', 'E': 'N', 'F': 'N'}

def ReadPorts():   
    i = 0
    for key in sorted(hubPorts): 
        hubPorts[key] = deviceTypeLookup.get(device.device_id(i))
        i+=1        
    return None
    
def is_connected(sensor):
    ReadPorts()
    listOfPorts = []
    is_a_connection = False
    i = 0
    for port in sorted(hubPorts):  
        if hubPorts[port] == sensor:
            is_a_connection = True
    return is_a_connection

def check_port(sensor):
    ReadPorts()
    listOfPorts = []
    is_a_connection = False
    i = 0
    for port in sorted(hubPorts):
        if hubPorts[port] == sensor:      
            is_a_connection = True
            return string2port(f"port.{port}")
    return None

    
def string2port(portS):
    if portS == "port.A": return port.A
    if portS == "port.B": return port.B
    if portS == "port.C": return port.C
    if portS == "port.D": return port.D
    if portS == "port.E": return port.E
    if portS == "port.F": return port.F

