import os

class View:
    def __init__(self):
        pass
    
    #Prompts user for input
    def getInputString(self):
        return input("What would you like to do?\n")
    
    #Calls all of the print functions for each specifc piece of hardware in the Hardware class. 
    #This should only print statistics that remain peristent on the computer, so things like the type of devices,
    #details surrounding the type of ram, cpu, network adapters, and storage space should be printed.
    def print_HW(self,hardware):
        self.clear()
        self.print_CPU(hardware.cpu)
        self.print_Memory(hardware.memory)
        self.print_Storage(hardware.storage)
        self.print_Network(hardware.network)
        user_input = input("Press enter to go back to the menu: ")
    
    #Self explanatory: This is the menu that allows our user to select the options they would like to use.
    def print_menu(self):
        self.clear()
        print("1. Show me my computers Hardware")
        print("2. View system performance (text)")
        print("3. View system performance (graph)")
        print("Enter \"q\" to quit")
    
    #Prints the persisting CPU statistics
    def print_CPU(self,cpu):
        print("CPU Info")
        print("Processor: " + cpu.name)
        print("Base Clock Rate: " + str(cpu.base_clock_rate))
        print("Number of Cores: " + str(cpu.num_of_cores))
        print()
    
    #Prints the persisting Network statistics
    def print_Network(self,network):
        print("Network Info")
        print("Total Bytes Sent: " + str(network.rx_bytes))
        print("Total Bytes Received: " + str(network.tx_bytes))
        print()
    
    #Prints the persisting Memory statistics
    def print_Memory(self,memory):
        print("Memory Info")
        print("Total: " + memory.total)
        print("Used: " + memory.used)
        print("Free: " + memory.free)
        print()
    
    #Prints the persisting Storage statistics
    def print_Storage(self,storage):
        print("Storage Info")
        print("Storage Device: " + storage.name)
        print("Size: " + storage.size)
        print("Available Space: " + storage.remaining_space)
        print("% Used: " + storage.percentage_used)
        print("Filesystem Type: " + storage.system_type)
        print()
    
    #Prints the statistics that are updated ever second of runtime. Things like thread-count, CPU utilization percentage, Ram utilization percentage,
    #current clock rate of CPU, current amount of memory being used.
    def print_statistics(self,hardware):
        # Print stats
        self.clear()
        print(f"CPU Utilization: {hardware.cpu.cpu_util}%")
        print(f"Memory Usage: {hardware.memory.mem_util.used / 1024**2:.2f} MiB / {hardware.memory.mem_util.total / 1024**2:.2f} MiB ({hardware.memory.mem_util.percent}%)")
        print(f"Disk I/O: Read Operations ={hardware.storage.storage_util.read_bytes / 2**20:.2f} MiB, Write Operations ={hardware.storage.storage_util.write_bytes / 2**20:.2f} MiB")
        print(f"Network Utilization: Bytes Receives ={hardware.network.net_util.bytes_recv / 2**20:.2f} MiB, Bytes Sent = {hardware.network.net_util.bytes_sent / 2**20:.2f} MiB")
        print("Press enter to go back to the menu: ")

    
    def plot_statistics(self,fig):
        # Display the chart
        fig.show()

        return fig
    
    def clear(self):
        os.system('clear')