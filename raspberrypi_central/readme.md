# Raspberrypi central
This is the raspberrypi (or other similar device), that will orchestrate a lot of things, this is the heart of the system.

## Burn the Raspbian image
I'm using [balena](https://www.balena.io/etcher/) to burn my images.

1. Download Raspbian image (please go to raspberry pi official website).
2. Burn the image on your sd card (:warning: choose the right disk, triple check)

So know we have the raspbian os ready to go!

## Setup connexion

### WiFi
To add network info you need to create a second text file called `wpa_supplicant.conf` and place that in the root of the boot SD as the `ssh` file.

```
country=FR
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="Your SSID"
    psk="YourWPAPassword"
    key_mgmt=WPA-PSK
}
```

### Find your raspberry pi on your LAN
When your raspberry is connected to your network (LAN), you'll be able to connect to it remotly through SSH. But to do so... We need its ip address, and to do so, I'm using `nmap` like so:

```
nmap -sn 192.168.1.0/24
```
Where `192.168.1.0/24` is my network ip/mask.

### SSH Keys
I suggest you (strongly recommend), to activate SSH connexion with ssh keys.
That can be done easily by the `keys.sh` script that will:
- generate a key pair (ed25519)
- send them on the rpi by ssh login@pi (you'll be asked the login & pi).
- create your ~/.ssh/config for you if you want to, so you can easily connect to your rpi by doing `ssh user@hostname`. The hostname will be asked.

This script is not bullet proof, this is my simple use case, how I create my keys. Simple but effective.

Note that I also use this script to setup ssh on my servers on my day to day basis.

## Raspi config
We need to configure a little bit the raspberry.
```
sudo raspi-config
```

- "Interfacing Optionns" -> "Camera" -> Enable camera accesss.
- "Advanced Options" -> Expan filesystem ensures that all of the SD card storage is available to the OS (then reboot).

## Install & Setup Docker

Run the script `install-docker.sh`.

Instead of running all your docker commands as `sudo`, we suggest you to add the `docker` group to the user. This is done by the `docker-install.sh` script. Here is the command to do it.
```
sudo usermod -aG docker $(whoami)
```

**Note that you have to disconnect/reconnect to apply group changes.**

## Global install
Run the script `install.sh`. It will install some useful software like docker-compose.
