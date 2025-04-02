# from opensplatlib import OpenSplat
# import time

# splats = []

# def connect(n):
#     s = OpenSplat(n)
#     s.connect()
#     splats.append(s)

# connect("52050F65-666E-BA3B-C583-685A0BD9A5F4")
# connect(None)

# for i in range(14):
#     index = 1 << i
#     # splats[0]
#     first_half = index & 0b11111111
#     second_half = index >> 8
#     splats[0].setLEDs(first_half, second_half, 255, 0, 0)
#     print(f'{i:>2}:{first_half:08b} {second_half:08b}')
#     time.sleep(1)

# splats[0].allLEDsOff()

#--------------------------- all BLE control --------------------------------
from pyscript import document, when
from pyscript.js_modules import ble_library

print("Hello, World!")


ble_info = document.getElementById("ble_info")
ble_connected = document.getElementById("ble_connected")

def received_ble(data):
    document.getElementById("ble_answer").innerHTML = 'received: '+data
    if myClient.connected and ble.connected and push.checked:
        myClient.publish(pub_topic.value, data)

ble = ble_library.newBLE()
ble.callback = received_ble

@when("click", "#ble_connect")
async def ask(event):
    name = 'Splat'
    if await ble.ask(name):
        print('name ',name)
        await ble.connect()
        print('connected!')
        ble_connected.innerHTML = 'connected'

@when("click", "#ble_disconnect")
async def on_disconnect(event):
    await ble.disconnect()
    print('disconnected')

@when("click", "#send_ble")
def on_send_ble(event):
    print(ble_info.value)
    ble.write(ble_info.value)