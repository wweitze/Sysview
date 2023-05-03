import time
import select
import sys

from view.view import View
from model.model import Hardware

class Controller:
    #Initialization function that generates the models and viewss. The model component is called hardware, 
    #as the only models we have all pertain to the computers hardware.
    def __init__(self):
        self.hardware = Hardware()
        self.view = View()
    
    #The main loop of the program. It is called at the start in main and simply runs until the user
    #enters q or Q in the menu.
    def start(self):
        while True:
            self.view.print_menu()
            response = self.view.getInputString()
            self.handle_menu_input(response)
    
    def stop(self):
        exit(0)
    
    #This is the hander for the menu function in the view module. 
    #Make changes to it how you see fit.
    def handle_menu_input(self,response: str):
        if response == "1":
            self.view.print_HW(self.hardware)
        elif response == "2":
            while True:
                # Check if user pressed Enter
                if select.select([sys.stdin,],[],[],0.0)[0]:
                    break
                self.view.print_statistics(self.hardware)
                # Wait for 1 second
                #time.sleep(1)
                self.update_concurrent_statistics()
        elif response == "3":
            self.view.clear()
            print("Please wait for 10 seconds while system utilization statistics are recorded.")
            fig = self.hardware.generateSystemGraphs()
            self.view.plot_statistics(fig)
        elif response == "q" or response == "Q":
            self.view.clear()
            self.stop()
        else:
            print("Please enter a valid option...")

    #This will be a function that we will call in the while loop when the user runs the option
    #to view real-time performance info. Here we will just call the updateStatistics function in model
    #to update the statistics in class objects that are real-time dependent
    def update_concurrent_statistics(self):
        self.hardware.updateHardwareUtilization()