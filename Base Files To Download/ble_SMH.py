# Base code for UART service from mpy examples

import bluetooth
import random
import struct
import time

from ble_advertising import decode_services, decode_name
from ble_advertising import advertising_payload

_IRQ_CENTRAL_CONNECT = 1
_IRQ_CENTRAL_DISCONNECT = 2
_IRQ_GATTS_WRITE = 3
_IRQ_GATTS_READ_REQUEST = 4
_IRQ_SCAN_RESULT = 5
_IRQ_SCAN_DONE = 6
_IRQ_PERIPHERAL_CONNECT = 7
_IRQ_PERIPHERAL_DISCONNECT = 8
_IRQ_GATTC_SERVICE_RESULT = 9
_IRQ_GATTC_SERVICE_DONE = 10
_IRQ_GATTC_CHARACTERISTIC_RESULT = 11
_IRQ_GATTC_CHARACTERISTIC_DONE = 12
_IRQ_GATTC_DESCRIPTOR_RESULT = 13
_IRQ_GATTC_DESCRIPTOR_DONE = 14
_IRQ_GATTC_READ_RESULT = 15
_IRQ_GATTC_READ_DONE = 16
_IRQ_GATTC_WRITE_DONE = 17
_IRQ_GATTC_NOTIFY = 18
_IRQ_GATTC_INDICATE = 19

_ADV_IND = 0x00
_ADV_DIRECT_IND = 0x01
_ADV_SCAN_IND = 0x02
_ADV_NONCONN_IND = 0x03

_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

_FLAG_READ = 0x0002
_FLAG_WRITE_NO_RESPONSE = 0x0004
_FLAG_WRITE = 0x0008
_FLAG_NOTIFY = 0x0010

_UART_UUID = _UART_SERVICE_UUID
_UART_TX = (_UART_TX_CHAR_UUID, _FLAG_READ | _FLAG_NOTIFY,)
_UART_RX = (_UART_RX_CHAR_UUID, _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,)
_UART_SERVICE = (_UART_UUID,(_UART_TX, _UART_RX),)

#------------------------------------Peripheral-------------------------------

class BLESimplePeripheral:
    def __init__(self, ble, type = 'UART', name="SPIKE"):
        self.type = type
        services = [_UART_UUID] if type == 'UART' else [_MIDI_UUID]
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        if self.type == 'UART':
            ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
            services = [_UART_UUID]
            print('setup as uart', name)
        else:
            ((self._handle_tx, ),) = self._ble.gatts_register_services((_MIDI_SERVICE,))
            self._handle_rx = self._handle_tx   # same handle for both directions
            services = [_MIDI_UUID]
            print('setup as midi')
        self._connections = set()
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=services)
        #self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            self._write_callback = None
            # Start advertising again to allow a new connection.
            #self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
                
    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def on_write(self, callback):
        self._write_callback = callback
        
    def disconnect(self):
        for conn_handle in self._connections:
            self._ble.gap_disconnect(conn_handle)

#------------------------------------Central-------------------------------
        
class BLESimpleCentral:   
    def __init__(self, target): 
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self.scanning = False
        self.target = target
        self.peripheral = None
        
    def _reset(self):
        # Cached name and address from a successful scan.
        self._name = None
        self._addr_type = None
        self._addr = None

        # Callbacks for completion of various operations.
        # These reset back to None after being invoked.
        self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None

        # Persistent callback for when new data is notified from the device.
        self._notify_callback = None

        # Connected device.
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._tx_handle = None
        self._rx_handle = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            self.read_scan(data)

        elif event == _IRQ_SCAN_DONE:
            if self.scanning:
                self.scanning = False
                self._ble.gap_scan(None)
                
        elif event == _IRQ_PERIPHERAL_CONNECT:
            # Connect successful.
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(self._conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Disconnect (either initiated by us or the remote end).
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                # If it was initiated by us, it'll already be reset.
                self._reset()

    def read_scan(self, data):
        addr_type, addr, adv_type, rssi, adv_data = data
        name = decode_name(adv_data)
        addr = bytes(addr)
        if name:
            if self.target in name:
                self.peripheral = name
                self._addr_type = addr_type
                self._addr = addr
                print("name: %s"%(name))
                self.stop_scan()
            
    def scan(self, duration = 2000):
        self.scanning = True
        return self._ble.gap_scan(duration, 30000, 30000)

    def wait_for_scan(self):
        while self.scanning:
            #print('.',end='')
            time.sleep(0.1)
        
    def stop_scan(self):
        self.scanning = False
        self._ble.gap_scan(None)
        
    def is_connected(self):
        return (self._conn_handle is not None and self._tx_handle is not None and self._rx_handle is not None)

            
    # Connect to the specified device (otherwise use cached address from a scan).
    def connect(self, addr_type=None, addr=None, callback=None):
        self._addr_type = addr_type or self._addr_type
        self._addr = addr or self._addr
        self._conn_callback = callback
        if self._addr_type is None or self._addr is None:
            return False
        self._ble.gap_connect(self._addr_type, self._addr)
        return True

    # Disconnect from current device.
    def disconnect(self):
        if not self._conn_handle:
            return
        self._ble.gap_disconnect(self._conn_handle)
        self._reset()

    # Send data over the UART
    def write(self, v, response=False):
        if not self.is_connected():
            return
        self._ble.gattc_write(self._conn_handle, self._rx_handle, v, 1 if response else 0)

    # Set handler for when data is received over the UART.
    def on_notify(self, callback):
        self._notify_callback = callback
