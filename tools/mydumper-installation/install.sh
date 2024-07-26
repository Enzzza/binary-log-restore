#!/bin/bash

# Install libatomic1 package
sudo apt-get install libatomic1

# Fetch latest release URL and extract version
release=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/mydumper/mydumper/releases/latest | cut -d'/' -f8)

# Download and install mydumper package
sudo wget https://github.com/mydumper/mydumper/releases/download/${release}/mydumper_${release:1}.$(lsb_release -cs)_amd64.deb
sudo dpkg -i mydumper_${release:1}.$(lsb_release -cs)_amd64.deb

# Remove installation
sudo rm mydumper_${release:1}.$(lsb_release -cs)_amd64.deb
