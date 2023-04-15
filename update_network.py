import re
import subprocess

def update_vagrantfile_and_inventory(interface, ip, subnet):
    with open("Vagrantfile", "r") as f:
        vagrantfile_lines = f.readlines()

    with open("Vagrantfile", "w") as f:
        for line in vagrantfile_lines:
            if "$network_interface =" in line:
                line = f"$network_interface = \"{interface}\"\n"
            f.write(line)

    with open("ansible_server/inventory.txt", "r") as f:
        inventory_lines = f.readlines()

    with open("ansible_server/inventory.txt", "w") as f:
        for idx, line in enumerate(inventory_lines):
            if "ansible_ssh_host=" in line:
                line = re.sub(
                    r"ansible_ssh_host=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
                    f"ansible_ssh_host={ip}",
                    line,
                )
                ip_parts = ip.split(".")
                ip_parts[-1] = str(int(ip_parts[-1]) + 1)
                ip = ".".join(ip_parts)
            inventory_lines[idx] = line
        f.writelines(inventory_lines)

try:
    ip_output = subprocess.check_output("ip addr", shell=True).decode('utf-8')
    iface_ip_match = re.search(r'(?P<iface>\w+):.*\n.*?inet\s*(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip_output)
    
    if iface_ip_match:
        iface = iface_ip_match.group("iface")
        ip = iface_ip_match.group("ip")
        if ip.startswith("172.17"):
            raise Exception("Docker IP address found. Ignoring.")
        subnet = "255.255.255.0"
        if ip.startswith("10."):
            subnet = "255.0.0.0"
        elif ip.startswith("172."):
            subnet = "255.240.0.0"
        elif ip.startswith("192.168."):
            subnet = "255.255.0.0"
        update_vagrantfile_and_inventory(iface, ip, subnet)
        print("Vagrantfile and inventory.txt updated.")
    else:
        raise Exception("Could not determine network interface or IP address.")
except Exception as e:
    print(f"Error: {e}")
