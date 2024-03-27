import subprocess

def check_free_space(drive, ram_to_add_mb):
    # Check if the selected drive has enough free space for virtual memory
    free_space_mb = int(subprocess.check_output(f"wmic logicaldisk where DeviceID='{drive}' get FreeSpace /value", shell=True).decode().split('=')[1]) / (1024**2)
    return free_space_mb >= ram_to_add_mb

def extend_ram(drive, ram_to_add_mb):
    # Calculate the total RAM needed (current RAM + additional RAM)
    total_ram_mb = int(subprocess.check_output("wmic computersystem get TotalPhysicalMemory /value", shell=True).decode().split('=')[1]) / (1024**2)
    total_ram_needed_mb = total_ram_mb + ram_to_add_mb
    
    # Check if the selected drive has enough space
    if not check_free_space(drive, ram_to_add_mb):
        print("Insufficient space on the selected drive.")
        return False
    
    # Set up virtual memory on the selected drive
    script = (
        f"$PageFileSize = {ram_to_add_mb}MB; "
        f"$Path = '{drive}\\pagefile.sys'; "
        "$PathTemp = '{drive}\\pagefile.temp'; "
        "$Pagefile = Get-WmiObject -Query \"SELECT * FROM Win32_PageFileSetting\"; "
        "$Pagefile | ForEach-Object { $_.Delete(); }; "
        "Set-WmiInstance -Class Win32_PageFileSetting -Arguments @{ Name = $PathTemp; MaximumSize = $PageFileSize * 2; }; "
        "Move-Item $PathTemp $Path; Restart-Computer -Force"
    )
    subprocess.run(["powershell", "-Command", script], shell=True)
    return True

def main():
    print("=== Virtual RAM Extension ===")
  # Drive name which will convert in RAM
    drive = ""
  #Ram size in mb
    ram_to_add_mb = 1000

    if extend_ram(drive, ram_to_add_mb):
        print("Virtual RAM setup complete.")
    else:
        print("Failed to setup virtual RAM.")

if __name__ == "__main__":
    main()
