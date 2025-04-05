#--------------------------- all BLE control --------------------------------
from pyscript import document, when, window
import splats
from opensplatlib import OpenSplat

print("Hello, World!")

def callback(data):
    window.console.log(data)
    data = [d for d in data]
    response_type = data[0]

    display = ''

    # TODO actually match this up to resultant data structure
    if response_type == 6: # battery case
        display = f'Battery is {data[2]}/100? or 255? not 100% sure'
    elif response_type == 0: # id case
        display = f'Splat id is {data[1]}'
    elif response_type == 5: # switch status case
        display = f'Switch status is {bin(data[2])}'
    elif response_type == 3: # pressed switch cae
        display = ''
        for i in range(4):
            color = "blue" if (data[2] >> i & 0b1) == 0b1 else "grey"
            document.getElementById(f"switch-{i + 1}").setAttribute("fill", color)
    else:
        print(f'uncaught response id {response_type}')

    if display != '':
        document.getElementById("ble_answer").innerHTML = display
        print(display)


myHub = splats.Hub()
myHub.callback(callback)

myHub.callback(callback)
# myHub.write(b'\x00\x10')  # get ID
@when("click", "#ble_connect")
async def ask(event):
    await myHub.connect('Splat')
    window.console.log('connected')

@when("click", "#ble_disconnect")
async def done(event):
    myHub.disconnect()
    window.console.log('disconnected')

opensplat = OpenSplat()

@when("click", "#battery")
async def battery_click(event):
    packet = opensplat.readBattery()
    await myHub.write(packet)
    print("Battery command sent:", packet)

@when("click", "#switches")
async def switches_click(event):
    packet = opensplat.readSwitches()
    await myHub.write(packet)
    print("Switches command sent:", packet)

@when("click", "#id")
async def id_click(event):
    packet = opensplat.identifySplat()
    await myHub.write(packet)
    print("Identify command sent:", packet)

@when("click", "#mute")
async def on_mute(event):
    await myHub.write(opensplat.soundOff())

@when("click", "#all-midi-off")
async def on_all_midi_off(event):
    await myHub.write(opensplat.allMIDIOff())

@when("click", "#all-off-btn")
async def on_all_leds_off(event):
    await myHub.write(opensplat.allLEDsOff())

@when("click", "#update-led-btn")
async def update_leds(event):
    for i in range(14):
        led_input = document.getElementById(f"led-{i}")
        if led_input:
            hex_color = led_input.value  # e.g. "#RRGGBB"
            # Convert the hex color to RGB integers.
            red = int(hex_color[1:3], 16)
            green = int(hex_color[3:5], 16)
            blue = int(hex_color[5:7], 16)
            # Determine which LED is being updated using bit masks.
            if i < 8:
                lowByte = 1 << i
                highByte = 0
            else:
                lowByte = 0
                highByte = 1 << (i - 8)
            packet = opensplat.setLEDs(lowByte, highByte, red, green, blue)
            await myHub.write(packet)
            print(f"LED {i} updated to RGB({red},{green},{blue}):", packet)

@when("click", "button.off-btn")
async def led_off_handler(event):
    # Extract the LED index from the button's id.
    button_id = event.target.id  # e.g. "led-off-3"
    try:
        index = int(button_id.split("-")[-1])
    except ValueError:
        print("Invalid LED off button id:", button_id)
        return

    # Compute the bit masks.
    if index < 8:
        lowByte = 1 << index
        highByte = 0
    else:
        lowByte = 0
        highByte = 1 << (index - 8)

    # Send the LED off command using the LEDsOff method.
    packet = opensplat.LEDsOff(lowByte, highByte)
    await myHub.write(packet)
    print(f"LED {index} Off command sent:", packet)


@when("click", "#all-off-btn")
async def all_leds_off(event):
    packet = opensplat.allLEDsOff()
    await myHub.write(packet)
    print("All LEDs Off command sent:", packet)

@when("click", "#mute")
async def mute_sound(event):
    packet = opensplat.soundOff()
    await myHub.write(packet)
    print("Sound Off command sent:", packet)

@when("change", "#volumeSlider")
async def volume_change(event):
    vol = int(document.getElementById("volumeSlider").value)
    packet = opensplat.setVolume(vol)
    await myHub.write(packet)
    print(f"Set Volume command with volume {vol} sent: {packet}")
    # TODO double check that the integer value is working the way I expect it to


# TODO implement checks that forces MIDI to be in correct range (or this could be done in HTML)
@when("click", "#note-on")
async def note_on(event):
    # Grab values from the form inputs. (Ensure the note input is numeric or adjust conversion accordingly.)
    note_val = int(document.getElementById("note").value)
    octave = int(document.getElementById("octave").value)
    velocity = int(document.getElementById("velocity").value)
    instrument = int(document.getElementById("instrument").value)
    packet = opensplat.noteOn(note_val, octave, velocity, instrument)
    await myHub.write(packet)
    print("Note On command sent:", packet)
    print(f"note val {note_val} octave {octave} vel {velocity} int {instrument}")


@when("click", "#note-off")
async def note_off(event):
    note_val = int(document.getElementById("note").value)
    octave = int(document.getElementById("octave").value)
    velocity = int(document.getElementById("velocity").value)
    instrument = int(document.getElementById("instrument").value)
    packet = opensplat.noteOff(note_val, octave, velocity, instrument)
    await myHub.write(packet)
    print("Note Off command sent:", packet)
    print(f"note val {note_val} octave {octave} vel {velocity} int {instrument}")


@when("click", "#all-midi-off")
async def all_midi_off(event):
    packet = opensplat.allMIDIOff()
    await myHub.write(packet)
    print("All MIDI Off command sent:", packet)


@when("click", "#play-sound")
async def play_sound(event):
    sound_index = int(document.getElementById("sound-index").value)
    vol = int(document.getElementById("volumeSlider").value)
    packet = opensplat.playSound(sound_index, vol)
    await myHub.write(packet)
    print(f"Played sound {sound_index} with volume {vol}: {packet}")


@when("click", "#test-click")
async def test_click(event):
    doorbell = [0x00,0x20,0x04,0xff]
    packet = doorbell
    await myHub.write(packet)
    print(f"Sent {packet}")