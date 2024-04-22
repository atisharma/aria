"""
Set up GPIO devices specific to Rosa.

- Three LEDs: red, green, yellow
- Toggle switches: left, right
- A rotary encoder with push button
"""

from time import sleep
import sys

from gpiozero import Button, RotaryEncoder, LED, CPUTemperature


green_led = LED(14)
red_led = LED(15)
yellow_led = LED(17)

# Using internal pull-up (the default), closed switch should ground GPIO4 (which is adjacent to ground pin).
switch_left = Button(5)
switch_right = Button(6)

# The rotary encoder has a 3-pin side (A, GND, B)
knob = RotaryEncoder(23, 26)
# and a 2-pin side (push button)
push_button = Button(27)

cpu = CPUTemperature()
