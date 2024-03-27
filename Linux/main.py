import subprocess

def check_free_space(drive, ram_to_add_mb):
    # Check if the selected drive has enough free space for virtual memory
    free_space_mb = int(subprocess.check_output(f"df -m {drive} | awk 'NR==2 {{print $4}}'", shell=True).decode().strip())
    return free_space_mb >= ram_to_add_mb

def extend_ram(drive, ram_to_add_mb):
    # Calculate the total RAM needed (current RAM + additional RAM)
    total_ram_mb = int(subprocess.check_output("grep MemTotal /proc/meminfo | awk '{print $2}'", shell=True).decode().strip()) // 1024
    total_ram_needed_mb = total_ram_mb + ram_to_add_mb
    
    # Check if the selected drive has enough space
    if not check_free_space(drive, ram_to_add_mb):
        return "Insufficient space on the selected drive."
    
    # Set up virtual memory on the selected drive
    subprocess.run(f"sudo dd if=/dev/zero of={drive}/pagefile bs=1M count={ram_to_add_mb}", shell=True)
    subprocess.run(f"sudo chmod 600 {drive}/pagefile", shell=True)
    subprocess.run(f"sudo mkswap {drive}/pagefile", shell=True)
    subprocess.run(f"sudo swapon {drive}/pagefile", shell=True)
    return "Virtual RAM setup complete."

def main():
    drive = "/mnt"
    ram_to_add_mb = 2048  # 2GB
    
    print("Starting Virtual RAM Extension...")
    result = extend_ram(drive, ram_to_add_mb)
    print(result)

if __name__ == "__main__":
    main()
