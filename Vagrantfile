# set up the default terminal
ENV["TERM"]="linux"

# set minimum version for Vagrant
Vagrant.require_version ">= 2.2.10"
Vagrant.configure("2") do |config|
  config.vm.provision "shell",
    inline: "sudo su - && zypper update && zypper install -y apparmor-parser"

  # Set the image for the vagrant box
  config.vm.box = "opensuse/Leap-15.2.x86_64"
  # Set the image version
  config.vm.box_version = "15.2.31.632"

  # Forward the ports from the guest VM to the local host machine
  # Forward more ports, as needed
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 6111, host: 6111
  config.vm.network "forwarded_port", guest: 6112, host: 6112
  config.vm.network "forwarded_port", guest: 6443, host: 6443
  for p in 30000..30100 # expose NodePort IP's
    config.vm.network "forwarded_port", guest: p, host: p, protocol: "tcp"
    end
  config.vm.provider "virtualbox" do |v|
    v.memory = "3072"
    v.name = "master"
    end
  config.vm.provision "shell", inline: <<-SHELL
    sudo zypper refresh
    sudo zypper --non-interactive install bzip2
    sudo zypper --non-interactive install etcd
    sudo zypper --non-interactive install apparmor-parser
    sudo zypper --non-interactive install git
    curl -sfL https://get.k3s.io | sh -
  SHELL

  # Set the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"

  # Configure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
