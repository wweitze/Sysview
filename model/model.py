from plotly.subplots import make_subplots
import plotly.graph_objs as go
import subprocess
import psutil

def parseString(hardware_str, start_str, end_str):
        start_index = hardware_str.find(start_str)
        if start_index == -1:
            return None
        
        end_index = hardware_str.find(end_str, start_index)
        if end_index == -1:
                return None
    
        start_index += len(start_str)  # exclude the start string itself
        return hardware_str[start_index:end_index].strip()

class Hardware:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.storage = Storage()
        self.network = Network()

    def updateHardwareUtilization(self):
        self.cpu.updateCPUUtilization()
        self.memory.updateMemoryUtilization()
        self.network.updateNetworkUtilization()
        self.storage.updateStorageUtilization()

    def generateSystemGraphs(self):
        # Initialize figure with subplots
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
        
        # Get initial utilization stats
        cpu_percent = psutil.cpu_percent(interval=10)
        mem = psutil.virtual_memory()
        
        # Create CPU utilization pie chart
        cpu_fig = go.Figure(data=[go.Pie(labels=['CPU Utilization', 'Idle'], values=[cpu_percent, 100-cpu_percent])])
        cpu_fig.update_traces(hole=.2, hoverinfo="label+percent")
        cpu_fig.update_layout(title="CPU Utilization")
        
        # Create memory utilization pie chart
        mem_fig = go.Figure(data=[go.Pie(labels=['Used Memory', 'Free Memory'], values=[mem.used, mem.available])])
        mem_fig.update_traces(hole=.2, hoverinfo="label+percent")
        mem_fig.update_layout(title="Memory Utilization")

        # Add pie charts to subplots
        fig.add_trace(cpu_fig.data[0], 1, 1)
        fig.add_trace(mem_fig.data[0], 1, 2)

        # Update layout of subplots
        fig.update_layout(
            title='System Utilization',
            grid=dict(rows=1, columns=2),
            annotations=[
                dict(text='CPU', x=0.21, y=0.5, font_size=20, showarrow=False),
                dict(text='Memory', x=0.8, y=0.5, font_size=20, showarrow=False)
            ]
        )
        
        return fig

class CPU:
    def __init__(self):
        self.name = None
        self.num_of_cores = None
        self.base_clock_rate = None
        self.cpu_string = None
        self.cpu_util = None
        self.getCPUInfo()
        self.updateCPUUtilization()

    def getCPUInfo(self):
        self.cpu_string = self.private_generate_cpu_info()
        self.name = parseString(self.cpu_string,"product:","\n")
        
        # Get the number of CPU cores
        num_cores_output = subprocess.check_output(["nproc"])
        self.num_of_cores = int(num_cores_output.strip())

        # Get the base clock rate of the CPU
        lscpu_output = subprocess.check_output(["lscpu"])
        for line in lscpu_output.splitlines():
            if b"MHz" in line:
                clock_rate_line = line.decode().strip()
                self.base_clock_rate = float(clock_rate_line.split(":")[1].strip())
                break
            
    def private_generate_cpu_info(self):
        result = subprocess.run(["sudo", "lshw", "-class", "cpu"], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    
    def updateCPUUtilization(self):
        self.cpu_util = psutil.cpu_percent(interval = 1)

class Memory:
    def __init__(self):
        self.total = None
        self.used = None
        self.free = None
        self.mem_util = None
        self.getMemoryInfo()
        self.updateMemoryUtilization()
        
    def getMemoryInfo(self):
        output = subprocess.check_output(["free", "-h"])

        lines = output.decode().strip().split("\n")
        line = lines[1]

        fields = line.split()
        self.total = fields[1]
        self.used = fields[2]
        self.free = fields[3]
    def updateMemoryUtilization(self):
        self.mem_util = psutil.virtual_memory()

class Storage:
    def __init__(self):
        self.name = None
        self.size = None
        self.remaining_space = None
        self.percentage_used = None
        self.system_type = None
        self.storage_util = None
        self.getStorageInfo()
        self.updateStorageUtilization()

    def getStorageInfo(self):
        output = subprocess.check_output(["df", "-h", "/dev/sda5"])

        lines = output.decode().strip().split("\n")
        line = lines[1]

        fields = line.split()
        self.name = fields[0]
        self.size = fields[1]
        self.remaining_space = fields[3]
        self.percentage_used= fields[4]

        cmd = ["lsblk", "-no", "fstype", "/dev/sda5"]
        output = subprocess.check_output(cmd).decode().strip()
        self.system_type = output
    def updateStorageUtilization(self):
        self.storage_util = psutil.disk_io_counters()

class Network:
    def __init__(self):
        self.rx_bytes = 0
        self.tx_bytes = 0
        self.net_util = None
        self.getBytesInfo()
        self.updateNetworkUtilization()

    def getBytesInfo(self):
        output = subprocess.check_output(["ifconfig"])

        lines = output.decode().strip().split("\n")
        for line in lines:
            if "RX packets" in line:
                fields = line.split()
                rx_bytes = fields[4]
                self.rx_bytes += int(rx_bytes)
            elif "TX packets" in line:
                fields = line.split()
                tx_bytes = fields[4]
                self.tx_bytes += int(tx_bytes)
        
        self.rx_bytes = self.rx_bytes / (1024 ** 2)
        self.tx_bytes = self.tx_bytes / (1024 ** 2)

        self.rx_bytes = round(self.rx_bytes, 2)
        self.tx_bytes = round(self.tx_bytes, 2)
    
    def updateNetworkUtilization(self):
        self.net_util = psutil.net_io_counters()