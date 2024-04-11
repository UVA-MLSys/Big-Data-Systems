import platform
import multiprocessing
import os

def get_hardware_details():
    """
    Retrieve basic hardware details of the system.

    Returns:
    dict: A dictionary containing the following hardware details:
        - 'System': The name of the operating system.
        - 'Node Name': The name of the node (typically the hostname).
        - 'Release': The operating system release.
        - 'Version': The operating system version.
        - 'Machine': The machine hardware name.
        - 'Processor': The processor type.
        - 'CPU Cores': The number of CPU cores.
        - 'CPU Vendor': The CPU vendor information.
        - 'CPU Model': The CPU model information.
        - 'RAM': The amount of RAM allocated to the job in gigabytes (if applicable).
    """
    details = {}
    
    details['System'] = platform.system()
    details['Node Name'] = platform.node()
    details['Release'] = platform.release()
    details['Version'] = platform.version()
    details['Machine'] = platform.machine()
    details['Processor'] = platform.processor()
    
    # Get number of CPU cores
    details['CPU Cores'] = len(os.sched_getaffinity(0))
    
    # Get CPU vendor and model
    cpu_info = {}
    with open('/proc/cpuinfo', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                key = parts[0].strip()
                value = parts[1].strip()
                cpu_info[key] = value
    details['CPU Vendor'] = cpu_info.get('vendor_id', 'N/A')
    details['CPU Model'] = cpu_info.get('model name', 'N/A')
    
    # Get amount of RAM allocated for the job (if applicable)
    allocated_ram_gb = None
    if 'SLURM_MEM_PER_NODE' in os.environ:
        slurm_mem_per_node = os.environ['SLURM_MEM_PER_NODE']
        allocated_ram_mb = int(slurm_mem_per_node.strip().split()[0])
        allocated_ram_gb = allocated_ram_mb / 1024.0  # Convert to gigabytes
    elif 'PBS_NUM_PPN' in os.environ:
        # Example for PBS/Torque, you may need to adjust based on your system
        num_ppn = int(os.environ['PBS_NUM_PPN'])
        total_ram_mb = psutil.virtual_memory().total / (1024.0 ** 2)  # Convert to megabytes
        allocated_ram_gb = total_ram_mb / num_ppn  # Divide by number of processes per node
    details['RAM'] = allocated_ram_gb
    
    return details