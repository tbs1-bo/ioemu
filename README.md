
# ioemu

![screenshot](ioemu-screenshot.png)

The ioemu-project provides a simple emulator for input output operations with simple elextronic components like LEDs and push buttons.

## Installation

Use pip for a simple installation

- Linux, MacOS: python3 -m pip install ioemu
- Windows: python -m pip install ioemu

## Examples

Import the emulator from the ioemu package


```python
from ioemu import Emulator
```

Create an instance of the emulator, write some bits into the buffer and show it with the `tick`-method. This method must be run periodically - e.g. in a loop.


```python
emu = Emulator(num_leds=3)
emu.write(0b101)
# run tick every frame
emu.tick()
```

## Buttons

The emulator contains two buttons. Their current state (pressed or not pressed) can be read from the attribute `button_pressed`. It's a bool array corresponding to the state of being pressed.


```python
emu = Emulator()  # 8 LEDs will be used if no number given
while True:
    if emu.button_pressed[0]:
        emu.write(0b11110000)
        
    if emu.button_pressed[1]:
        emu.write(0b00001111)

    emu.tick()
```

## Counter

Finally a counter, that counts up when pressing one button and down, when pressing the other.


```python
emu = Emulator()
i = 1
while True:
    if emu.button_pressed[0]:
        i += 1
    if emu.button_pressed[1]:
        i -= 1

    # fit i into range of values
    i = i % 255

    emu.write(i)
    emu.tick()
```
