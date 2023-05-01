import os
import re
import subprocess

# Function to get default network interface
def get_default_interface():
    route_output = subprocess.check_output(["ip", "route"]).decode("utf-8")
    default_interface = None
    for line in route_output.split("\n"):
        if "default" in line:
            default_interface = line.split()[4]
            break

    if default_interface is None:
        return None

    # Check if the default interface has a global IPv4 address
    addr_output = subprocess.check_output(["ip", "addr", "show", default_interface]).decode("utf-8")
    for line in addr_output.split("\n"):
        if "inet " in line and not "scope link" in line:
            return default_interface

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

ip_pattern = re.compile(r'ip: "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"')
file_contents = ip_pattern.sub(lambda match: f'ip: "{base_ip}{match.group(1).split(".")[-1]}"', file_contents)

with open("Vagrantfile", "w") as f:
    f.write(file_contents)

# Update inventory file
inventory_file_path = "inventory.txt"  # Modify this line to the correct location of your inventory.txt file
with open(inventory_file_path, "r") as f:
    file_contents = f.read()

inventory_pattern = re.compile(r"ansible_ssh_host=(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
updated_file_contents = inventory_pattern.sub(lambda match: f"ansible_ssh_host={base_ip}{match.group(1).split('.')[-1]}", file_contents)

with open(inventory_file_path, "w") as f:
    f.write(updated_file_contents)

print("Successfully updated Vagrantfile and inventory.txt")
