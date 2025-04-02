class OpenSplat:
    """
    Class to interface with Splats
    """

    def keepAlive(self):
        """
        0x01   Keep Alive reset 3 second and 5 minute timers
        """
        packet = [0x01, 0x00]
        return bytearray(packet)

    def soundOff(self):
        """
        0x02   Sound Off   Turn sound off
        """
        packet = [0x02, 0x00]
        return bytearray(packet)

    def allLEDsOff(self):
        """
        0x03   LEDs Off    Turn all LEDs Off
        """
        packet = [0x03, 0x00]
        return bytearray(packet)

    def allTasksOff(self):
        """
        0x04  All Off Turn all tasks off
        """
        packet = [0x04, 0x00]
        return bytearray(packet)

    def readSwitches(self):
        """
        0x05  Read Switches   Read switch state and send Response and 8 bit data to App
        """
        packet = [0x05, 0x00]
        return bytearray(packet)

    def readBattery(self):
        """
        0x06  Read Battery    Read Battery voltage  and send Response and 8 bit data to App
        """
        packet = [0x06, 0x00]
        return bytearray(packet)

    def uploadLEDAnimation(self):
        """
        0x07  Upload LED Animation    Upload the LED Animation Table from APP to SPI Flash
        """
        packet = [0x07, 0x00]
        return bytearray(packet)

    def enterUploadVoiceMode(self):
        """
        0x08  Upload Voice    Upload the Voice from APP to SPI Flash
        """
        packet = [0x08, 0x00]
        return bytearray(packet)

    def enterUpdateFirmwareMode(self):
        """
        0x09  Update Firmware Update the firmware from APP to SPI Flash
        """
        packet = [0x09, 0x00]
        return bytearray(packet)

    def requestFirmwareVersion(self):
        """
        0x0A  Request Firmware Version    Return firmware version
        """
        packet = [0x0A, 0x00]
        return bytearray(packet)

    def resetBLEModuleOnSplat(self):
        """
        0x0B Reset BLE module Resets BLE module
        """
        packet = [0x0B, 0x00]
        return bytearray(packet)

    def allMIDIOff(self):
        """
        0x0C  All MIDI channels NoteOff   Sends noteOff to all notes on all 4 MIDI channels
        """
        packet = [0x0C, 0x00]
        return bytearray(packet)

    def identifySplat(self):
        """
        0x1000    ID #    Identify    ID # value  None
        """
        packet = [0x00, 0x10]
        return bytearray(packet)

    def setVolume(self, vol):
        """
        0x1001    Vol #   Volume setting  Volume # value TBD  None
        """
        packet = [0x01, 0x10, vol]
        return bytearray(packet)

    def playSound(self, soundIndex, vol):
        """
        0x2000    Sound # Volume Level    Play Sound  Play system sound effect # send response when complete  Command
        """
        packet = [0x00, 0x20, soundIndex, vol]
        return bytearray(packet)

    def playRecordedSound(self, soundIndex, vol):
        """
        ?0x2001    Sound # Volume Level    Play Game Sound Play uploaded sound #index 80 - 87 send response when complete  Command
        """
        packet = [0x01, 0x20, soundIndex, vol]
        return bytearray(packet)

    def noteOn(self, note, octave, velocity, instrument):
        """
        0x4000    Note    Octave  Velocity    Instrument / Timbre Play MIDI Note or Chord
        This command receive to NoteOn, the channel will dynamic to play
        """
        packet = [0x00, 0x40, note, octave, velocity, instrument]
        return bytearray(packet)

    def noteOff(self, note, octave, velocity, instrument):
        """
        0x4001    Note    Octave  Velocity    Instrument / Timbre Turn Off MIDI Note or Chord
        This command must same to NoteOn Command which note you want to NoteOFF.
        """
        packet = [0x01, 0x40, note, octave, velocity, instrument]
        return bytearray(packet)

    def LEDsOff(self, lowByte, highByte):
        """
        0x2004    LED 0 to 7 turn  off 0 indicates OFF    LED 8 to 13turn  off 0 indicates OFF    LED OFF Turn LEDs off
        Only turn off the LEDs with 0 Indication   None
        """
        packet = [0x04, 0x20, lowByte, highByte]
        return bytes(packet)

    def setLEDs(self, lowByte, highByte, red, green, blue):
        """
        5001  LED 0 to 7
        Turn On 1 indicates ON    LED 8 to 13
        Turn On 1 indicates ON    Red intensity   Green Intensity Blue  intensity Turn LED On Set color of LED # 0 to 13  indicated by 2 8 bit boolean
        Only change the state of LEDs with 1 indication   Command NA
        Only turn off the LEDs with 0 Indication    None
        """
        packet = [0x01, 0x50, lowByte, highByte, red, green, blue]
        return bytearray(packet)

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
        return bytearray(packet)

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
        return bytearray(packet)
