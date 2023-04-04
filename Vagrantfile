# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provider "vmware_desktop" do |v|
    v.vmx["numvcpus"] = "2"
    v.vmx["memsize"] = "2048"
  end

  config.vm.define "ansible" do |ansible|
    ansible.vm.box = "generic/ubuntu2004"
    ansible.vm.hostname = "config-server"
    ansible.vm.network "public_network", bridge: $network_interface, ip: "192.168.245.2", netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    ansible.vm.synced_folder ".", "/vagrant", type: "rsync"
    ansible.vm.provision "shell", inline: <<-SHELL
      sudo apt update
      sudo apt install software-properties-common
      sudo apt-add-repository ppa:ansible/ansible
      sudo apt update
      sudo apt install ansible
    SHELL
    ansible.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "/home/badtux/Desktop/ansible_k8s_jenkins_docker/Ansible/ansible/ansible.yml"
    end
  end

  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.box = "generic/ubuntu2004"
    jenkins.vm.hostname = "jenkins"
    jenkins.vm.network "public_network", bridge: $network_interface, ip: "192.168.245.3", netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    jenkins.vm.synced_folder ".", "/vagrant", type: "rsync"
    jenkins.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "/home/badtux/Desktop/ansible_k8s_jenkins_docker/Ansible/jenkins/jenkins.yml"
    end
  end

  config.vm.define "k8s" do |k8s|
    k8s.vm.box = "generic/ubuntu2004"
    k8s.vm.hostname = "k8s"
    k8s.vm.network "public_network", bridge: $network_interface, ip: "192.168.245.4", netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    k8s.vm.synced_folder ".", "/vagrant", type: "rsync"
    k8s.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "/home/badtux/Desktop/ansible_k8s_jenkins_docker/Ansible/k8s/k8s.yml"
    end
  end
end
