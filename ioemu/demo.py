import os
import time

import ioemu

# Port to which the demo client talks
# Can be overriden by an environmental variable.
DEMO_CLIENT_PORT = int(os.environ.get('IOEMU_DEMO_CLIENT_PORT', default=ioemu.TCP_SERVER_PORT))


emu = ioemu.Emulator(port=DEMO_CLIENT_PORT)
last_btn_state = emu.buttons
last_analog_val = emu.analog_value
last_update = time.time()
counter = 0

while True:
    if time.time() - last_update > 0.4:
        emu.leds = [b == '1' for b in bin(counter)[2:].zfill(3)]
        counter = (counter + 1) % 8
        last_update = time.time()

    if emu.buttons != last_btn_state:
        last_btn_state = emu.buttons
        print("Buttons:", last_btn_state)

    if emu.analog_value != last_analog_val:
        last_analog_val = emu.analog_value
        print("Analog Value:", last_analog_val)
