import sys
from pkg_resources import resource_filename
import subprocess

filepath = resource_filename(__name__, 'sounds/' + 'alarm-clock-elapsed.wav')


class Playme():
    def __init__(self):
        #self.wf = wave.open(filepath, 'rb')
        self.wf = filepath

    def play(self):
        subprocess.Popen(["paplay", self.wf])
