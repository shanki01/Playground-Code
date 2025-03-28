#!/usr/bin/env python
import random
import functools
from datetime import datetime, date, time
from enum import Enum

from bluepy import btle

UUID_CHARACTERISTIC_RECV = btle.UUID('fff4')
UUID_CHARACTERISTIC_WRITE = btle.UUID('fff3')

def connection_required(func):
    """Raise an exception before calling the actual function if the device is
    not connected.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._connection is None:
            raise Exception("Not connected")

        return func(self, *args, **kwargs)

    return wrapper


def _figure_addr_type(mac_address=None, version=None, addr_type=None):
    return btle.ADDR_TYPE_PUBLIC


class OpenSplat:
    
    """
    Class to interface with Splats
    """

    def __init__(self, mac_address, version=1, addr_type=None):
        """
        :param mac_address: device MAC address as a string
        :param version: bulb version as displayed in official app (integer)
        """
        self._connection = None

        self.mac_address = mac_address
        self.version = version
        self._addr_type = _figure_addr_type(mac_address, version, addr_type)

        self.__time_schedule_buffer = None

        self._device_info = {}
        self._date_time = None
        self._time_schedule = []

    def connect(self, bluetooth_adapter_nr=0):
        """
        Connect to device
        
        :param bluetooth_adapter_nr: bluetooth adapter name as shown by
            "hciconfig" command. Default : 0 for (hci0)
        
        :return: True if connection succeed, False otherwise
        """

        try:
            connection = btle.Peripheral(self.mac_address, self._addr_type,
                                         bluetooth_adapter_nr)
            self._connection = connection.withDelegate(self)
            self._subscribe_to_recv_characteristic()
        except RuntimeError as e:
            return False

        return True

    def disconnect(self):
        """
        Disconnect from device
        """

        try:
            self._connection.disconnect()
        except btle.BTLEException:
            pass

        self._connection = None

    def is_connected(self):
        """
        :return: True if connected
        """
        return self._connection is not None  # and self.test_connection()

    def test_connection(self):
        """
        Test if the connection is still alive
        
        :return: True if connected
        """
        if not self.is_connected():
            return False

        # send test message, read bulb name
        try:
            self.get_device_name()
        except btle.BTLEException:
            self.disconnect()
            return False
        except BrokenPipeError:
            # bluepy-helper died
            self._connection = None
            return False

        return True

    @connection_required
    def get_device_name(self):
        """
        :return: Device name
        """
        buffer = self._device_name_characteristic.read()
        buffer = buffer.replace(b'\x00', b'')
        return buffer.decode('ascii')

    def handleNotification(self, handle, buffer):

        if len(buffer) >= 11 and buffer[0] == 0x66 and buffer[11] == 0x99:
            self._device_info = Protocol.decode_device_info(buffer)
        elif len(buffer) >= 10 and buffer[0] == 0x13 and buffer[10] == 0x31:
            self._date_time = Protocol.decode_date_time(buffer)
        elif len(buffer) >= 20 and buffer[0] == 0x25:  # start time_schedule
            self.__time_schedule_buffer = bytearray(buffer)
        elif self.__time_schedule_buffer is not None:  # reading time_schedule
            self.__time_schedule_buffer += buffer
            if len(self.__time_schedule_buffer) >= 87:
                self._time_schedule = Protocol.decode_time_schedule(
                        self.__time_schedule_buffer)
                self.__time_schedule_buffer = None

    def __str__(self):
        return "<MagicBlue({}, {})>".format(self.mac_address, self.version)

    @property
    def _send_characteristic(self):
        """Get BTLE characteristic for sending commands"""
        characteristics = self._connection.getCharacteristics(
                uuid=UUID_CHARACTERISTIC_WRITE)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _recv_characteristic(self):
        """Get BTLE characteristic for receiving data"""
        characteristics = self._connection.getCharacteristics(
                uuid=UUID_CHARACTERISTIC_RECV)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _device_name_characteristic(self):
        """Get BTLE characteristic for reading device name"""
        # characteristics = self._connection.getCharacteristics(
        #         uuid=UUID_CHARACTERISTIC_DEVICE_NAME)
        if not characteristics:
            return None
        return characteristics[0]

    def _subscribe_to_recv_characteristic(self):
        char = self._recv_characteristic
        handle = char.valHandle + 1
        msg = bytearray([0x01, 0x00])
        self._connection.writeCharacteristic(handle, msg)

    def keepAlive(self):
               # 0x01   Keep Alive reset 3 second and 5 minute timers
       packet = [ 0x01, 0x00 ];
       self._send_characteristic.write(bytearray(packet))
       
    def soundOff(self):
               # 0x02   Sound Off   Turn sound off
       packet = [ 0x02, 0x00 ];
       self._send_characteristic.write(bytearray(packet))
    
    def allLEDsOff(self):
               # 0x03   LEDs Off    Turn all LEDs Off
       packet = [ 0x03, 0x00 ];
       self._send_characteristic.write(bytearray(packet))
    
    def allTasksOff(self):
                # 0x04  All Off Turn all tasks off
       packet = [ 0x04, 0x00 ];
       self._send_characteristic.write(bytearray(packet))
    
    def readSwitches(self):
                # 0x05  Read Switches   Read switch state and send Response and 8 bit data to App
        packet = [ 0x05, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def readBattery(self):
                # 0x06  Read Battery    Read Battery voltage  and send Responce and 8 bit data to App
        packet = [ 0x06, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def uploadLEDAnimation(self):
                # 0x07  Upload LED Animation    Upload the LED Animation Table from APP to SPI Flash
        packet = [ 0x07, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def enterUploadVoiceMode(self):
                # 0x08  Upload Voice    Upload the Voice from APP to SPI Flash
        packet = [ 0x08, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def enterUpdateFirmwareMode(self):
                # 0x09  Update Firmware Update the firmware from APP to SPI Flash
        packet = [ 0x09, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def requestFirmwareVersion(self):
                # 0x0A  Request Firmware Version    Return firmware version
        packet = [ 0x0A, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def resetBLEModuleOnSplat(self):
                # 0x0B Reset BLE module Resets BLE module
        packet = [ 0x0B, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def allMIDIOff(self):
                # 0x0C  All MIDI channels NoteOff   Sends noteOff to all notes on all 4 MIDI channels
        packet = [ 0x0C, 0x00 ];
        self._send_characteristic.write(bytearray(packet))
    
    def identifySplat(self):
                # 0x1000    ID #    Identify    ID # value  None
        packet = [ 0x00, 0x10 ];
        self._send_characteristic.write(bytearray(packet))
    
    def setVolume(self, vol):
                # 0x1001    Vol #   Volume setting  Volume # value TBD  None
        packet = [ 0x01, 0x10, vol];
        self._send_characteristic.write(bytearray(packet))
    
    def playSound(self, soundIndex, vol):
                # 0x2000    Sound # Volume Level    Play Sound  Play system sound effect # send response when complete  Command
        packet = [ 0x00, 0x20, soundIndex, vol ];
        self._send_characteristic.write(bytearray(packet))
    
    def playRecordedSound(self, soundIndex, vol):
                # 0x2001    Sound # Volume Level    Play Game Sound Play uploaded sound #index 80 - 87 send response when complete  Command
        packet = [ 0x01, 0x20, soundIndex, vol ];
        self._send_characteristic.write(bytearray(packet))
    
    def noteOn(self, note, velocity, instrument):
                # 0x4000    Note    Octave  Velocity    Instrument / Timbre Play MIDI Note or Chord 
        # This command receive to NoteOn, the channel will dynamic to play
        packet = [ 0x00, 0x40, note, octave, velocity, instrument ];
        self._send_characteristic.write(bytearray(packet))
        
    def noteOff(note, velocity, instrument):
                # 0x4001    Note    Octave  Velocity    Instrument / Timbre Turn Off MIDI Note or Chord 
        # This command must same to NoteOn Command which note you want to NoteOFF. 
        packet = [ 0x01, 0x40, note, octave, velocity, instrument ];
        self._send_characteristic.write(bytearray(packet))
    
    def LEDsOff(self, lowByte, highByte):
                # 0x2004    LED 0 to 7 turn  off 0 indicates OFF    LED 8 to 13turn  off 0 indicates OFF    LED OFF Turn LEDs off 
        #Only turn off the LEDs with 0 Indication   None
        packet = [ 0x04, 0x20, lowByte, highByte ];
        self._send_characteristic.write(bytearray(packet))
     
    def setLEDs(self, lowByte, highByte, red, green, blue):
                # 5001  LED 0 to 7
        # Turn On 1 indicates ON    LED 8 to 13
        # Turn On 1 indicates ON    Red intensity   Green Intensity Blue  intensity Turn LED On Set color of LED # 0 to 13  indicated by 2 8 bit boolean 
        # Only change the state of LEDs with 1 indication   Command NA 
        #Only turn off the LEDs with 0 Indication    None
        packet = [ 0x01, 0x50, lowByte, highByte, red, green, blue ];
        self._send_characteristic.write(bytearray(packet))   
    
    def playLEDSequence(self, seqIndex, red, green, blue, duration, loops):
                # 0x6001    Sequence
        # # Red intensity   Green Intensity Blue  intensity Duration in 10ms    Number of loops
        # 0 to 255  Play light sequence 
        #   # is sequence number
        # Intensity is 0 to 255 RGB intensity 
        # Duration is time between  steps in 10m Sec increments and repet the sequence for number of loops
        # Send response when sequence complete  Command
        packet = [ 0x01, 0x60, seqIndex, red, green, blue, duration, loops ];
        self._send_characteristic.write(bytearray(packet))
    
    def flashLEDs(self, lowByte, highByte, red, green, blue, duration, flashes):
                # 0x7000    LED 0 to 7
        # Flash State
        # 1 indicates Flash LED 8 to 13
        # Flash State
        # 1 indicates Flash Red intensity   Green Intensity Blue  intensity Duration  in 20ms   # of flashes
        # 0 to 255  Flash LED   Flash LEDs for the time indicated
        # in the duration and repeat for number of flashes.
        # Send Response to App when completed   Command None
        packet = [ 0x01, 0x70, lowByte, highByte, red, green, blue, duration, flashes ];
        self._send_characteristic.write(bytearray(packet))
    
    

