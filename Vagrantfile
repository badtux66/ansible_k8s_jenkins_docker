# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'socket'
require 'timeout'

$network_interface = `sudo iw dev | awk '$1=="Interface"{print $2}'`.strip
$subnet = `ip -4 addr show $network_interface | awk '/inet 192.168./{split($2,a,"."); print a[3]}'`.strip

def get_available_ip(base_ip, subnet)
  ip_parts = base_ip.split(".")
  ip_parts[2] = subnet
  (1..254).each do |octet|
    ip_parts[3] = octet.to_s
    candidate_ip = ip_parts.join(".")
    begin
      timeout(1) { TCPSocket.new(candidate_ip, 22) }
    rescue Errno::ETIMEDOUT, Errno::ECONNREFUSED, Timeout::Error, Errno::EHOSTUNREACH
      return candidate_ip
    end
  end
  raise "No available IP addresses in the subnet"
end

Vagrant.configure("2") do |config|
  config.vm.provider "vmware_desktop" do |v|
    v.vmx["numvcpus"] = "2"
    v.vmx["memsize"] = "2048"
  end

  config.vm.define "ansible" do |ansible|
    ansible.vm.box = "generic/ubuntu2004"
    ansible.vm.hostname = "config-server"
    ansible_ip = get_available_ip("192.168.#{$subnet}.2", $subnet)
    ansible.vm.network "public_network", bridge: $network_interface, ip: ansible_ip, netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    ansible.vm.synced_folder ".", "/vagrant", type: "rsync"
    ansible.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/ansible.yml"
    end
  end

  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.box = "generic/ubuntu2004"
    jenkins.vm.hostname = "jenkins"
    $subnet = $subnet.to_i + 1
    jenkins_ip = get_available_ip("192.168.#{$subnet}.3", $subnet)
    jenkins.vm.network "public_network", bridge: $network_interface, ip: jenkins_ip, netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    jenkins.vm.synced_folder ".", "/vagrant", type: "rsync"
    jenkins.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "jenkins/jenkins.yml"
    end
  end

  config.vm.define "k8s" do |k8s|
    k8s.vm.box = "generic/ubuntu2004"
    k8s.vm.hostname = "k8s"
    $subnet = $subnet.to_i + 1
    k8s_ip = get_available_ip("192.168.#{$subnet}.4", $subnet)
    k8s.vm.network "public_network", bridge: $network_interface, ip: k8s_ip, netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    k8s.vm.synced_folder ".", "/vagrant", type: "rsync"
    k8s.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "k8s/k8s.yml"
    end
  end
end
