
from sploitkit import *
import subprocess
import sys

class Clear(Command):
    def run(self):
        #TODO: compute results here
        subprocess.run('clear')
        pass
