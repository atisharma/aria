import sys
from time import sleep
from functools import partial
from pathlib import Path
from threading import Event

import numpy as np
from PIL import Image, ImageSequence, ImageFont

from rosa import oled, volume
from rosa.devices import knob, switch_left, switch_right, push_button, green_led, red_led, yellow_led


###################################
#    Service functions            #
###################################

def show_connection(device, font, font_size, text):
    """
    Show connection status,
    """
    with oled.canvas(device) as draw:
        pass

def show_vol(device, font, font_size):
    """
    Show the volume bar.
    """
    v = volume.get()
    with oled.canvas(device) as draw:
        draw.font = font
        draw.fontmode = "L"
        oled.filled_bar(draw, (4, 10, device.width - 10, font_size), 0.01 * v, f"volume: {v:d}", font)

def show_status(device, font, font_size, text):
    with oled.canvas(device) as draw:
        oled.status_text(draw, (4, 10, device.width - 10, font_size), text, font)


###################################
#    Event callbacks / bindings   #
###################################

def volume_up(device, font, font_size):
    volume.up()
    show_vol(device, font, font_size)

def volume_down(device, font, font_size):
    volume.down()
    show_vol(device, font, font_size)

def mic_off(device, font, font_size):
    """
    Sleep the display and turn off the mic.
    """
    volume.mic_off()
    red_led.on()
    green_led.off()
    show_status(device, font, font_size, "microphone off\ndisplay sleeping")
    sleep(0.5)
    device.hide()

def mic_on(device, font, font_size):
    """
    Wake the display and mic.
    """
    volume.mic_on()
    red_led.off()
    green_led.on()
    device.show()
    show_status(device, font, font_size, "microphone on")

def bind_events(device, font, font_size):
    # set callbacks
    knob.when_rotated_clockwise = partial(volume_up, device, font, font_size)
    knob.when_rotated_counter_clockwise = partial(volume_down, device, font, font_size)

    # pipewire mute
    push_button.when_released = volume.mute

    # left switch should toggle listening
    if switch_left.is_active:
        mic_off(device, font, font_size)
    else:
        mic_on(device, font, font_size)
    switch_left.when_pressed = partial(mic_off, device, font, font_size)
    switch_left.when_released = partial(mic_on, device, font, font_size)


class Ui:
    def __init__(self, params=None):
        self.params = params or {}
        self.kill = False

        # oled-related things
        self.device = oled.get_device(self.params.get('luma_args'))
        self.term_font_size = 12
        self.term_font = ImageFont.truetype(str(Path(__file__).resolve().parent.joinpath("fonts", "spleen-6x12.otf")), self.term_font_size)
        self.large_font_size = 24
        self.large_font = ImageFont.truetype(str(Path(__file__).resolve().parent.joinpath("fonts", "spleen-12x24.otf")), self.large_font_size)
        #self.large_font = ImageFont.truetype(str(Path(__file__).resolve().parent.joinpath("fonts", "monof56.ttf")), self.large_font_size)

        self.term = oled.terminal(self.device, self.term_font)
        self.term.animate = True

        bind_events(self.device, self.large_font, self.large_font_size)

        self.load_visual("system_init")
        
    def update_visual(self, user_name, data, time_color_warning=0):
        if not switch_right.is_active:
            if user_name == "You":
                oled.plot_data(self.device, data, scale=1.2)
            elif user_name == "Aria":
                oled.plot_data(self.device, data)
            
    def load_visual(self, user_name):
        if user_name == "system_init":
            self.add_message("system", "waking...\n", new_entry=True)
        elif user_name == "system_transition":
            self.add_message("system", "\n", new_entry=True)
        elif user_name == "system_muted_mic":
            self.add_message("system", "microphone muted\n", new_entry=True)
        elif user_name == "You":
            yellow_led.on()
        elif user_name == "Aria":
            yellow_led.off()
    
    def add_message(self, user_name, text, new_entry=False, color_code_block=False, code_blocks=[]):
        if switch_right.is_active:
            if new_entry:
                self.term.println()
            self.term.puts(text)
            self.term.flush()
    
    def start(self):
        events = Event()
        try:
            print("waiting for UI events...")
            events.wait()

        except KeyboardInterrupt:
            print("exit")
            self.kill = True
            events.set()

        except Exception as err:
            self.kill = True
            print(err)
            sys.exit(1)
