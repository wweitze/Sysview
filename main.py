# Checklist for things to add to the program:
# -Gather System Hardware Information (RAM, CPU, GPU, ETC)
# -Display Syystem Performance Statistics (Process Count, CPU Usage, GPU Usage, Network Usage, Disk Usage, Memory Usage, ETC)
# -Allow users to kill processes
#
# The first 2 things take priority. We mainly just want to get as much information about the system as possible1

from controller.controller import Controller

if __name__ == '__main__':
    controller = Controller()
    
    controller.start()