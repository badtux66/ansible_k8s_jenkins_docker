import os
import subprocess

# Function to get default network interface
def get_default_interface():
    route_output = subprocess.check_output(["ip", "route"]).decode("utf-8")
    for line in route_output.split("\n"):
        if "default" in line:
            return line.split()[4]
    return None

# Get default network interface and IP address
default_interface = get_default_interface()
if default_interface is None:
    print("Unable to find the default network interface.")
    exit(1)

ip_output = subprocess.check_output(["ip", "addr", "show", default_interface]).decode("utf-8")
ip_address = ""
for line in ip_output.split("\n"):
    if "inet " in line:
        ip_address = line.strip().split()[1].split("/")[0]
        break

if not ip_address:
    print("Unable to find IP address associated with the default network interface.")
    exit(1)

# Determine the network based on the IP address
ip_parts = ip_address.split(".")
base_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}."

# Update Vagrantfile
with open("Vagrantfile", "r") as f:
    file_contents = f.read()

file_contents = file_contents.replace('ip: "192.168.174.2"', f'ip: "{base_ip}2"')
file_contents = file_contents.replace('ip: "192.168.174.3"', f'ip: "{base_ip}3"')
file_contents = file_contents.replace('ip: "192.168.174.5"', f'ip: "{base_ip}5"')

with open("Vagrantfile", "w") as f:
    f.write(file_contents)

# Update inventory file
inventory_file_path = "ansible_server/inventory.txt"
with open(inventory_file_path, "r") as f:
    file_contents = f.read()

updated_file_contents = file_contents.replace("ansible_ssh_host=192.168.174.2", f"ansible_ssh_host={base_ip}2")
updated_file_contents = updated_file_contents.replace("ansible_ssh_host=192.168.174.3", f"ansible_ssh_host={base_ip}3")
updated_file_contents = updated_file_contents.replace("ansible_ssh_host=192.168.174.5", f"ansible_ssh_host={base_ip}5")

with open(inventory_file_path, "w") as f:
    f.write(updated_file_contents)

print("Successfully updated Vagrantfile and inventory.txt")
