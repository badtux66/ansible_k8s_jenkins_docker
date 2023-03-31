require 'socket'
require 'timeout'

def get_network_interface
  default_route_line = `ip route | grep "default via"`
  raise "Could not find default route. Make sure you have a default route configured and try again." if default_route_line.nil?
  default_route_interface = default_route_line.split("dev ")[1].split(":")[0].strip
  default_route_interface
end

$network_interface = get_network_interface

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  # Configuration Management VM
  config.vm.define "ansible" do |ansible|
    ansible.vm.hostname = "ansible"
    ansible.vm.network "public_network", bridge: $network_interface, auto_config: true
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
  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.hostname = "jenkins"
    jenkins.vm.network "public_network", bridge: $network_interface, auto_config: true
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
  config.vm.define "k8s" do |k8s|
    k8s.vm.hostname = "k8s"
    k8s.vm.network "public_network", bridge: $network_interface, auto_config: true
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
