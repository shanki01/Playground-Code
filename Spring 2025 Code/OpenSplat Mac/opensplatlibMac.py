#!/usr/bin/env python
import asyncio
import functools
from bleak import BleakClient, BleakScanner

class OpenSplatMac:
    """
    Class to interface with Splats
    """

    def __init__(self, address, version=1, addr_type=None):
        """
        :param address: device MAC address as a string
        :param version: bulb version as displayed in official app (integer)
        """
        self.address = address
        self.client = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.UUID_CHARACTERISTIC_RECV = 'fff4'
        self.UUID_CHARACTERISTIC_WRITE = 'fff3'

    async def _find_first_splat(self, max_retries=3):
        for attempt in range(max_retries):
            print(f"Scanning for SPLAT devices... (Attempt {attempt + 1}/{max_retries})")
            devices = await BleakScanner.discover()

            for device in devices:
                if device.name in ["SPLAT", "Splat"]:
                    print(f"Found {device.name} ({device.address})")
                    return device.address

            print("No SPLAT devices found")

        print("Failed to find SPLAT device after multiple attempts.")
        return None

    async def _connect(self, max_retries=3):
        address = self.address

        if not address:
            address = await self._find_first_splat()
            if not address:
                print("Connection failed: No device found.")
                return False
        for attempt in range(max_retries):
            try:
                self.client = BleakClient(address)
                await self.client.connect()
                print(f"Connected to {address}")
                return True
            except Exception as e:
                self.client = None
                print(f"Failed to connect (Attempt {attempt + 1}/{max_retries}): {e}")

        print(f"Failed to connect after multiple attempts.")
        return False

    def connect(self, bluetooth_adapter_nr=0):
        """
        Connect to device

        :return: True if connection succeed, False otherwise
        """
        return self.loop.run_until_complete(self._connect())

    async def _disconnect(self):
        if self.client and self.client.is_connected:
            try:
                await self.client.disconnect()
                print("Disconnected")
            except Exception as e:
                print(f"Disconnection failed ({e})")
            finally:
                self.client = None

    def disconnect(self):
        """
        Disconnect from device
        """
        self.loop.run_until_complete(self._disconnect())

    def is_connected(self):
        """
        :return: True if connected
        """
        return self.client and self.client.is_connected

    def get_device_name(self):
        """
        :return: Device name
        """
        # buffer = self._device_name_characteristic.read()
        # buffer = buffer.replace(b'\x00', b'')
        # return buffer.decode('ascii')
        return None

    def handleNotification(self, handle, buffer):
        # if len(buffer) >= 11 and buffer[0] == 0x66 and buffer[11] == 0x99:
        #     self._device_info = Protocol.decode_device_info(buffer)
        # elif len(buffer) >= 10 and buffer[0] == 0x13 and buffer[10] == 0x31:
        #     self._date_time = Protocol.decode_date_time(buffer)
        # elif len(buffer) >= 20 and buffer[0] == 0x25:  # start time_schedule
        #     self.__time_schedule_buffer = bytearray(buffer)
        # elif self.__time_schedule_buffer is not None:  # reading time_schedule
        #     self.__time_schedule_buffer += buffer
        #     if len(self.__time_schedule_buffer) >= 87:
        #         self._time_schedule = Protocol.decode_time_schedule(
        #             self.__time_schedule_buffer)
        #         self.__time_schedule_buffer = None
        pass

    def __str__(self):
        return "<MagicBlue({})>".format(self.address)

    def write_data(self, data):
        if not self.is_connected():
            print("Not connected. Attempting to reconnect...")
            self.connect()

        try:
            self.loop.run_until_complete(
                self.client.write_gatt_char(self.UUID_CHARACTERISTIC_WRITE, data, response=True)
            )

            print(f"Data written successfully: {data}")
        except Exception as e:
            print(f"Failed to write data ({e})")

    @property
    def _recv_characteristic(self):
        """Get BTLE characteristic for receiving data"""
        # characteristics = self._connection.getCharacteristics(
        #     uuid=UUID_CHARACTERISTIC_RECV)
        # if not characteristics:
        #     return None
        # return characteristics[0]
        return None

    @property
    def _device_name_characteristic(self):
        """Get BTLE characteristic for reading device name"""
        # characteristics = self._connection.getCharacteristics(
        #         uuid=UUID_CHARACTERISTIC_DEVICE_NAME)
        # if not characteristics:
        #     return None
        # return characteristics[0]
        return None

    def _subscribe_to_recv_characteristic(self):
        # char = self._recv_characteristic
        # handle = char.valHandle + 1
        # msg = bytearray([0x01, 0x00])
        # self._connection.writeCharacteristic(handle, msg)
        pass

    def keepAlive(self):
        """
        0x01   Keep Alive reset 3 second and 5 minute timers
        """
        packet = [0x01, 0x00]
        self.write_data(bytearray(packet))

    def soundOff(self):
        """
        0x02   Sound Off   Turn sound off
        """
        packet = [0x02, 0x00]
        self.write_data(bytearray(packet))

    def allLEDsOff(self):
        """
        0x03   LEDs Off    Turn all LEDs Off
        """
        packet = [0x03, 0x00]
        self.write_data(bytearray(packet))

    def allTasksOff(self):
        """
        0x04  All Off Turn all tasks off
        """
        packet = [0x04, 0x00]
        self.write_data(bytearray(packet))

    def readSwitches(self):
        """
        0x05  Read Switches   Read switch state and send Response and 8 bit data to App
        """
        packet = [0x05, 0x00]
        self.write_data(bytearray(packet))

    def readBattery(self):
        """
        0x06  Read Battery    Read Battery voltage  and send Response and 8 bit data to App
        """
        packet = [0x06, 0x00]
        self.write_data(bytearray(packet))

    def uploadLEDAnimation(self):
        """
        0x07  Upload LED Animation    Upload the LED Animation Table from APP to SPI Flash
        """
        packet = [0x07, 0x00]
        self.write_data(bytearray(packet))

    def enterUploadVoiceMode(self):
        """
        0x08  Upload Voice    Upload the Voice from APP to SPI Flash
        """
        packet = [0x08, 0x00]
        self.write_data(bytearray(packet))

    def enterUpdateFirmwareMode(self):
        """
        0x09  Update Firmware Update the firmware from APP to SPI Flash
        """
        packet = [0x09, 0x00]
        self.write_data(bytearray(packet))

    def requestFirmwareVersion(self):
        """
        0x0A  Request Firmware Version    Return firmware version
        """
        packet = [0x0A, 0x00]
        self.write_data(bytearray(packet))

    def resetBLEModuleOnSplat(self):
        """
        0x0B Reset BLE module Resets BLE module
        """
        packet = [0x0B, 0x00]
        self.write_data(bytearray(packet))

    def allMIDIOff(self):
        """
        0x0C  All MIDI channels NoteOff   Sends noteOff to all notes on all 4 MIDI channels
        """
        packet = [0x0C, 0x00]
        self.write_data(bytearray(packet))

    def identifySplat(self):
        """
        0x1000    ID #    Identify    ID # value  None
        """
        packet = [0x00, 0x10]
        self.write_data(bytearray(packet))

    def setVolume(self, vol):
        """
        0x1001    Vol #   Volume setting  Volume # value TBD  None
        """
        packet = [0x01, 0x10, vol]
        self.write_data(bytearray(packet))

    def playSound(self, soundIndex, vol):
        """
        0x2000    Sound # Volume Level    Play Sound  Play system sound effect # send response when complete  Command
        """
        packet = [0x00, 0x20, soundIndex, vol]
        self.write_data(bytearray(packet))

    def playRecordedSound(self, soundIndex, vol):
        """
        ?0x2001    Sound # Volume Level    Play Game Sound Play uploaded sound #index 80 - 87 send response when complete  Command
        """
        packet = [0x01, 0x20, soundIndex, vol]
        self.write_data(bytearray(packet))

    def noteOn(self, note, octave, velocity, instrument):
        """
        0x4000    Note    Octave  Velocity    Instrument / Timbre Play MIDI Note or Chord
        This command receive to NoteOn, the channel will dynamic to play
        """
        packet = [0x00, 0x40, note, octave, velocity, instrument]
        self.write_data(bytearray(packet))

    def noteOff(self, note, octave, velocity, instrument):
        """
        0x4001    Note    Octave  Velocity    Instrument / Timbre Turn Off MIDI Note or Chord
        This command must same to NoteOn Command which note you want to NoteOFF.
        """
        packet = [0x01, 0x40, note, octave, velocity, instrument]
        self.write_data(bytearray(packet))

    def LEDsOff(self, lowByte, highByte):
        """
        0x2004    LED 0 to 7 turn  off 0 indicates OFF    LED 8 to 13turn  off 0 indicates OFF    LED OFF Turn LEDs off
        Only turn off the LEDs with 0 Indication   None
        """
        packet = [0x04, 0x20, lowByte, highByte]
        self.write_data(bytes(packet))

    def setLEDs(self, lowByte, highByte, red, green, blue):
        """
        5001  LED 0 to 7
        Turn On 1 indicates ON    LED 8 to 13
        Turn On 1 indicates ON    Red intensity   Green Intensity Blue  intensity Turn LED On Set color of LED # 0 to 13  indicated by 2 8 bit boolean
        Only change the state of LEDs with 1 indication   Command NA
        Only turn off the LEDs with 0 Indication    None
        """
        packet = [0x01, 0x50, lowByte, highByte, red, green, blue]
        self.write_data(bytearray(packet))

    def playLEDSequence(self, seqIndex, red, green, blue, duration, loops):
        """
        0x6001    Sequence
        # Red intensity   Green Intensity Blue  intensity Duration in 10ms    Number of loops
        0 to 255  Play light sequence
          # is sequence number
        Intensity is 0 to 255 RGB intensity
        Duration is time between  steps in 10m Sec increments and repeat the sequence for number of loops
        Send response when sequence complete  Command
        """
        packet = [0x01, 0x60, seqIndex, red, green, blue, duration, loops]
        self.write_data(bytearray(packet))

    def flashLEDs(self, lowByte, highByte, red, green, blue, duration, flashes):
        """
        0x7000    LED 0 to 7
        Flash State
        1 indicates Flash LED 8 to 13
        Flash State
        1 indicates Flash Red intensity   Green Intensity Blue  intensity Duration  in 20ms   # of flashes
        0 to 255  Flash LED   Flash LEDs for the time indicated
        in the duration and repeat for number of flashes.
        Send Response to App when completed   Command None
        """
        packet = [0x01, 0x70, lowByte, highByte, red, green, blue, duration, flashes]
        self.write_data(bytearray(packet))
