import re
from subprocess import Popen, check_output

def up():
    Popen(["amixer", "-q", "-D", "pipewire", "sset", "Master", "1%+"])

def down():
    Popen(["amixer", "-q", "-D", "pipewire", "sset", "Master", "1%-"])

def mute():
    Popen(["amixer", "-q", "-D", "pipewire", "sset", "Master", "toggle"])

def mic_on():
    Popen(["amixer", "-q", "-D", "pipewire", "sset", "Capture", "cap"])

def mic_off():
    Popen(["amixer", "-q", "-D", "pipewire", "sset", "Capture", "nocap"])

def get():
    output = check_output(["amixer", "-D", "pipewire", "get", "Master"])
    vol = int(re.search(r"([0-9]+)%", output.decode()).group(1))
    return vol
