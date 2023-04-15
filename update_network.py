import os
import subprocess

# Run "ip addr" command and get the network interface name and IP address
ip_output = subprocess.check_output(["ip", "addr"]).decode("utf-8")
network_interface = ""
ip_address = ""
for line in ip_output.split("\n"):
    if "inet " in line:
        ip_address = line.strip().split()[1].split("/")[0]
    elif "state UP" in line:
        network_interface = line.strip().split(":")[1].strip()

# Determine the network based on the IP address
network = ""
first_octet = int(ip_address.split(".")[0])
if 192 <= first_octet <= 223:
    network = f"{first_octet}.0.0.0/8"
elif 128 <= first_octet <= 191:
    network = f"{first_octet}.0.0/16"
else:
    network = f"{first_octet}.0/24"

# Update Vagrantfile
with open("Vagrantfile", "r") as f:
    file_contents = f.read()
file_contents = file_contents.replace('$network_interface = "1: lo"', f'$network_interface = "{network_interface}"')
file_contents = file_contents.replace('bridge: "$network_interface"', f'bridge: "{network}"')
with open("Vagrantfile", "w") as f:
    f.write(file_contents)

# Update inventory file
with open("inventory.txt", "r") as f:
    file_contents = f.read()
file_contents = file_contents.replace("ansible_ssh_host=192.168.174.2", f"ansible_ssh_host={ip_address}")
with open("inventory.txt", "w") as f:
    f.write(file_contents)
    
print("Successfully updated Vagrantfile and inventory.txt")
