import os

class LinuxSystemInfo():

    def __init__(self):
        self.system = os.popen('cat /etc/*-release | grep "^ID="', 'r').read()
        self.processor = os.popen(' cat /proc/cpuinfo | grep "model name"', 'r').read()
        self.memory = os.popen('free -h', 'r').read()
        self.diskspace = os.popen('df -h | grep "/dev"', 'r').read()
        self.shell = os.getenv('SHELL')
        self.kernel = os.system('uname -a')

# To DO:  Work on commands below - self.processor
class MacOSSystemInfo():

    def __init__(self):
        self.system = os.popen('uname', 'r').read()
        # self.processor = os.popen(' cat /proc/cpuinfo | grep "model name"', 'r').read()
        # self.memory = os.popen('free -h', 'r').read()
        self.diskspace = os.popen('df -h | grep "/dev"', 'r').read()
        self.shell = os.getenv('SHELL')
        self.kernel = os.system('uname -a')