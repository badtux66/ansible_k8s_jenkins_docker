
$network_interface = "wlan0"

Vagrant.configure("2") do |config|
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

  config.vm.define "ansible" do |ansible|
    ansible.vm.box = "generic/ubuntu2004"
    ansible.vm.hostname = "config-server"
    ansible.vm.network "public_network", bridge: $network_interface, ip: "192.168.220.2", netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    ansible.vm.synced_folder "/home/badtux/Desktop/ansible_k8s_jenkins_docker", "/vagrant", type: "rsync", rsync__exclude: ".git/"

    ansible.vm.provision "shell", inline: <<-SHELL
      sudo apt update
      sudo apt install -y software-properties-common
      sudo apt-add-repository -y ppa:ansible/ansible
      sudo apt update
      sudo apt install -y ansible
      sudo apt install -y open-vm-tools
      sudo apt install -y rsync
    SHELL

    ansible.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "Ansible/ansible/ansible.yml"
    end
  end

  config.vm.define "jenkins" do |jenkins|
    jenkins.vm.box = "generic/ubuntu2004"
    jenkins.vm.hostname = "jenkins"
    jenkins.vm.network "public_network", bridge: $network_interface, ip: "192.168.220.3", netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    jenkins.vm.synced_folder "/home/badtux/Desktop/ansible_k8s_jenkins_docker", "/vagrant", type: "rsync", rsync__exclude: ".git/"

    jenkins.vm.provision "shell", inline: <<-SHELL
      sudo apt update
      sudo apt update
      sudo apt install -y open-vm-tools
      sudo apt install -y rsync
    SHELL

    jenkins.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "Ansible/jenkins/jenkins.yml"
    end
  end

  config.vm.define "k8s" do |k8s|
    k8s.vm.box = "generic/ubuntu2004"
    k8s.vm.hostname = "k8s"
    k8s.vm.network "public_network", bridge: $network_interface, ip: "192.168.220.5", netmask: "255.255.255.0", use_dhcp_assigned_default_route: true
    k8s.vm.synced_folder "/home/badtux/Desktop/ansible_k8s_jenkins_docker", "/vagrant", type: "rsync", rsync__exclude: ".git/"

    k8s.vm.provision "shell", inline: <<-SHELL
      sudo apt update
      sudo apt update
      sudo apt install -y open-vm-tools
      sudo apt install -y rsync
    SHELL
    
    k8s.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "Ansible/k8s/k8s.yml"
    end
  end
end
