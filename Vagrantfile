require 'socket'
require 'timeout'

$network_interface = `sudo iw dev | awk '$1=="Interface"{print $2}'`.strip
$subnet = `ip -4 addr show $network_interface | awk '/inet 192.168./{split($2,a,"."); print a[3]}'`.strip

def get_available_ip(base_ip, subnet)
  ip_parts = base_ip.split(".")
  ip_parts[2] = subnet
  (ip_parts[3].to_i..254).each do |octet|
    ip_parts[3] = octet.to_s
    candidate_ip = ip_parts.join(".")
    begin
      timeout(1) { TCPSocket.new(candidate_ip, 22) }
    rescue Errno::ETIMEDOUT, Errno::ECONNREFUSED, Timeout::Error
      return candidate_ip
    end
  end
  raise "No available IP addresses in the subnet"
end

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  # Configuration Management VM
  ansible_ip = get_available_ip("192.168.#{$subnet}.10", $subnet)
  config.vm.define "ansible" do |ansible|
    ansible.vm.hostname = "ansible"
    ansible.vm.network "public_network", bridge: "wlan0", ip: ansible_ip, dhcp:true
    ansible.vm.provider "vmware_desktop" do |v|
      v.name = "ansible"
      v.memory = 1024
      v.cpus = 1
    end
    ansible.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "/home/badtux/Desktop/ansible_k8s_jenkins_docker/ansible/ansible.yml"
    end
  end

  # CI/CD VM
  jenkins_ip = get_available_ip("192.168.#{$subnet}.20", $subnet)
  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.hostname = "jenkins"
    jenkins.vm.network "public_network", bridge: "wlan0", ip: jenkins_ip, dhcp: true
    jenkins.vm.provider "vmware_desktop" do |v|
      v.name = "jenkins"
      v.memory = 2048
      v.cpus = 2
    end
    jenkins.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "/home/badtux/Desktop/ansible_k8s_jenkins_docker/jenkins/jenkins.yml"
    end
  end

  # Kubernetes VM
  k8s_ip = get_available_ip("192.168.#{$subnet}.30", $subnet)
  config.vm.define "k8s" do |k8s|
    k8s.vm.hostname = "k8s"
    k8s.vm.network "public_network", bridge: "wlan0", ip: k8s_ip, dhcp: true
    k8s.vm.provider "vmware_desktop" do |v|
      v.name = "k8s"
      v.memory = 2048
      v.cpus = 2
    end
    k8s.vm.provision "ansible" do |ansible|
      ansible.limit = "all"
      ansible.playbook = "/home/badtux/Desktop/ansible_k8s_jenkins_docker/k8s/k8s.yml"
    end
  end
end
