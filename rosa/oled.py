"""
High-level functions to put data to the oled screen.
"""

import time
import sys
import numpy

from PIL import ImageFilter

from luma.core.render import canvas
from luma.core import cmdline, error
from luma.core.virtual import viewport, terminal


def display_settings(device, args):
    """
    Display a short summary of the settings.
    """
    iface = ''
    display_types = cmdline.get_display_types()
    if args.display not in display_types['emulator']:
        iface = f'Interface: {args.interface}\n'

    lib_name = cmdline.get_library_for_display_type(args.display)
    if lib_name is not None:
        lib_version = cmdline.get_library_version(lib_name)
    else:
        lib_name = lib_version = 'unknown'

    import luma.core
    version = f'luma.{lib_name} {lib_version} (luma.core {luma.core.__version__})'

    return f'Version: {version}\nDisplay: {args.display}\n{iface}Dimensions: {device.width} x {device.height}\n{"-" * 60}'

def get_device(actual_args):
    """
    Create device from the command-line arguments or config and return it.
    """
    print("Luma display arguments:", * actual_args)
    parser = cmdline.create_parser(description='luma arguments')
    args = parser.parse_args(actual_args)

    # create device
    try:
        device = cmdline.create_device(args)
        print(display_settings(device, args))
        return device

    except error.Error as e:
        parser.error(e)
        return None

def filled_bar(draw, coords, fraction, text, font, radius=2, above=False):
    """
    Draw a bar, filled up to the fraction, with a text legend, at the coords.
    """
    [x, y, w, h] = coords
    fw = round(fraction * w)
    margin = 5
    [_, _, w_text, h_text] = font.getbbox(text)
    x_text = x + w - w_text - margin
    if fraction > 0:
        draw.rounded_rectangle((x, y, x + fw, y + h), radius=radius, fill="white")
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, outline="white")
    if above or (h < h_text):
        draw.text((x, y - h_text - margin), text, fill="white")
    else:
        # Switch to left when the occluded text would be less
        occluded_left = max(0, min(w_text - fw, w_text, w))
        occluded_right = max(0, min(fw + w_text - w, w_text, w))
        if occluded_right > occluded_left:
            draw.text((x + margin, y + 1), text, fill="black")
        else:
            draw.text((x_text, y + 1), text, fill="white")

def status_text(draw, coords, text, font):
    """
    Draw text at the coords.
    """
    [x, y, w, h] = coords
    margin = 5
    [_, _, w_text, h_text] = font.getbbox(text)
    x_text = x + w - w_text - margin
    draw.text((x, y - margin), text, font=font, fill="white")

def scroll_message(device, message, font=None, speed=1):
    """
    Scroll some text right to left.
    """
    x = device.width

    # First measure the text size
    with canvas(device) as draw:
        left, top, right, bottom = draw.textbbox((0, 0), message, font)
        w, h = right - left, bottom - top

    virtual = viewport(device, width=max(x, w + x + x), height=max(h, device.height))
    with canvas(virtual) as draw:
        draw.text((x, 0), message, font=font, fill="white")

    i = 0
    while i < x + w:
        virtual.set_position((i, 0))
        i += speed
        time.sleep(0.025)

def plot_data(device, data, scale=0.8):
    """
    Simple line plot of data, no axes.
    Suitable for showing a waveform.
    """
    # plot only the last data points, smoothed,
    # and rescale to [0, h]
    d = numpy.convolve(data, numpy.ones(8)/8.0, 'valid')
    if numpy.abs(d.max()) > 0.015:
        d = scale * device.height * d + (device.height / 2)
        l = min(d.size, device.width)
        with canvas(device) as draw:
            for i in range(l):
                y = int(d[int(i * device.width / l)])
                draw.point((i, y + 1), fill="#666666")
                draw.point((i, y), fill="#FFFFFF")
                draw.point((i, y - 1), fill="#666666")

def swipe(device):
    for i in range(device.width):
        with canvas(device) as draw:
            draw.line([(i, 0), (i, device.height)], fill="white", width=2)

    
