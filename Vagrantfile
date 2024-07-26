# Database servers
MYSQL_SERVER1_NAME = "mysql-server1"
MYSQL_SERVER2_NAME = "mysql-server2"
MYSQL_SERVER3_NAME = "mysql-server3"
MARIADB_SERVER1_NAME = "mariadb-server1"

MYSQL_SERVER1_IP = "192.168.56.10"
MYSQL_SERVER2_IP = "192.168.56.11"
MYSQL_SERVER3_IP = "192.168.56.12"
MARIADB_SERVER1_IP = "192.168.56.13"

def installutils()
  utils = <<-SCRIPT
    sudo apt update
    sudo apt install software-properties-common
    sudo apt install -y curl wget socat jq net-tools tmux
    sudo apt-get install libatomic1
  SCRIPT
end

Vagrant.configure("2") do |config|
  # General VM configuration
  config.vm.box = "generic/ubuntu2204"
  config.ssh.username = "vagrant"
  config.ssh.password = "vagrant"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end
  if Vagrant.has_plugin?("vagrant-cachier")
      config.cache.scope = :box
      config.cache.enable :apt
  end

  config.vm.define MYSQL_SERVER1_NAME do |mysql_server1_name|
    mysql_server1_name.vm.hostname = "#{MYSQL_SERVER1_NAME}"
    mysql_server1_name.vm.network "private_network", ip: "#{MYSQL_SERVER1_IP}"
    mysql_server1_name.vm.synced_folder "tools/", "/home/vagrant/tools"
    mysql_server1_name.vm.provision "shell", inline: installutils(), privileged: true
  end

  config.vm.define MYSQL_SERVER2_NAME do |mysql_server2_name|
    mysql_server2_name.vm.hostname = "#{MYSQL_SERVER2_NAME}"
    mysql_server2_name.vm.network "private_network", ip: "#{MYSQL_SERVER2_IP}"
    mysql_server2_name.vm.synced_folder "tools/", "/home/vagrant/tools"
    mysql_server2_name.vm.provision "shell", inline: installutils(), privileged: true
  end

  config.vm.define MYSQL_SERVER3_NAME do |mysql_server3_name|
    mysql_server3_name.vm.hostname = "#{MYSQL_SERVER3_NAME}"
    mysql_server3_name.vm.network "private_network", ip: "#{MYSQL_SERVER3_IP}"
    mysql_server3_name.vm.synced_folder "tools/", "/home/vagrant/tools"
    mysql_server3_name.vm.provision "shell", inline: installutils(), privileged: true
  end

  config.vm.define MARIADB_SERVER1_NAME do |mariadb_server1_name|
    mariadb_server1_name.vm.hostname = "#{MARIADB_SERVER1_NAME}"
    mariadb_server1_name.vm.network "private_network", ip: "#{MARIADB_SERVER1_IP}"
    mariadb_server1_name.vm.synced_folder "tools/", "/home/vagrant/tools"
    mariadb_server1_name.vm.provision "shell", inline: installutils(), privileged: true
  end
end
