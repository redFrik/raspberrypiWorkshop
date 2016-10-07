# raspberrypiWorkshop

held at [ems](http://elektronmusikstudion.se) 9oct2016, organized by [vems](https://vems.nu)

in this 3h workshop we will install the raspbian operating system from scratch, install pure data and supercollider and last look at how to connect an arduino board and send data to/from it from the raspberry pi.

**participants should bring:**

* laptop - preferably with sd card reader/writer
* micro sd card - 8gb or larger
* raspberry pi - model 1b, 2 or 3
* power supply - 5v microusb for the rpi
* headphones with minijack
* ethernet cable
* arduino with usb cable

**additional:** (_but not necessary_)

* usb sound card
* usb wlan module
* breadboard, sensors, leds, wires

overview
==

1. [burn raspbian to your sd card](burn_raspbian_to_your_sd_card)
2. [start your raspberry pi](start_your_raspberry_pi)
3. [log in to your raspberry pi](log_in_to_your_raspberry_pi)
4. [setup raspbian](setup_raspbian)
5. [installing pure data](installing_pure_data)
6. [installing supercollider](installing_supercollider)
7. [tune your audio](tune_your_audio)
8. [autostart](autostart)
9. [communicate with arduino](communicate_with_arduino)
10. [useful terminal commands](useful_terminal_commands)
11. [shutdown button](shutdown_button)

burn raspbian to your sd card
--

1. download the latest [raspbian image](https://www.raspberrypi.org/downloads/raspbian/)
    - (_or copy the zip from the provided usbstick_)
    - (_here we use 2016-05-27-raspbian-jessie.img - not the 'lite' version_)
    - (_jessie 'lite' will fit on a smaller sd card and is useful for non-gui headless systems_)
    - (_to save space you can use the .zip file directly without unpacking the .img_)
2. download [etcher.io](http://etcher.io)
    - (_mac, linux, windows_)
    - (_you can also use [pifiller](http://ivanx.com/raspberrypi/)_)
3. start etcher
4. select the raspbian zip file
5. insert your 8gb sd card
6. click flash
    - (_on my machine the process takes ~9min_)

![etcher](etcher.png)

start your raspberry pi
--

1. put the sd card in your raspberry pi
2. connect the ethernet cable
    - (_the other end goes to your home wlan router or to your laptop_)
    - (_if to your mac laptop: go to system preferences / network and activate internet sharing - share from wifi to ethernet_)
    - (_if to your windows machine: see [here](http://raspberrypi.stackexchange.com/questions/11684/how-can-i-connect-my-pi-directly-to-my-pc-and-share-the-internet-connection)_)
3. connect 5v micro usb
    - (_always connect power last_)
    - (_on first boot the rpi will automatically expand the file system_)

log in to your raspberry pi
--

1. wait a bit after applying 5v
    - (_specially on first boot it will take a while to connect to the network_)
2. find your raspberry pi on the network
    - (_we want to see that it is accessible and which ip address it got assigned_)
    - (_log in to your router's admin setup panel_)
    - (_on osx you can use [lanscan](https://www.iwaxx.com/lanscan)_)
3. open terminal and type `ssh pi@raspberry`
    - (_terminal is also called console. on osx it is found under applications/utilities_)
    - (_if you get a warning about remote host identification first do `ssh-keygen -R raspberrypi`_)
    - (_or try `ssh pi@raspberrypi.local` or `pi@192.168.1.52` or whatever ip address you saw in your router/lanscan search in #2 above_)
4. default password 'raspberry'
5. type 'exit' to leave

![login](login.png)

setup raspbian
--

1. log in again using ssh
    - (_see #3 above_)
2. type `sudo raspi-config`
3. change user password
    - advanced options / hostname
    - advanced options / memory split
    - advanced options / vnc

real [vnc viewer](https://www.realvnc.com/download/viewer/)

reference: setting up wifi via command line... https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

installing pure data
--

see <http://www.fredrikolofsson.com/f0blog/?q=node/630>

installing supercollider
--

see <https://github.com/redFrik/supercolliderStandaloneRPI2>

tune your audio
--

```bash
set alsavolume:
alsamixer
amixer
```

autostart
--

```bash
crontab -e
```

arduino
--

```cpp
//arduino code
void setup() {
    Serial.begin(57600);
}
void loop() {
    int val = analogRead(A0);
    Serial.write(253);
    Serial.write(254);
    Serial.write(val>>8);
    Serial.write(val&255);
    Serial.write(255);
    delay(100);  //update rate
}
```

```bash
apt-cache search "^pd-"
sudo apt-get install pd-comport pd-cyclone
```

pure data patch. save as ```pdarduino.pd```
```
#N canvas 141 95 450 300 10;
#X msg 86 31 devices;
#X obj 86 61 comport 1 57600;
#X obj 86 95 cyclone/match 253 254 nn nn 255;
#X obj 86 140 unpack f f f f f;
#X obj 140 176 << 8;
#X obj 140 202 +;
#X floatatom 140 230 5 0 0 0 - - -, f 5;
#X connect 0 0 1 0;
#X connect 1 0 2 0;
#X connect 2 0 3 0;
#X connect 3 2 4 0;
#X connect 3 3 5 1;
#X connect 4 0 5 0;
#X connect 5 0 6 0;
```

```python
import serial
ser= serial.Serial('/dev/ttyUSB0', 57600)
while True:
    print ser.readline()
```

```
a= SerialPort("/dev/ttyUSB0", 57600);
r= Routine.run({999.do{var h= a.read; var l= a.read; (h<<8+l).postln}})
```

useful terminal commands
--

```bash
ls          #list files
df -h       #disk free
free -h     #ram memory
top         #cpu usage (quit with 'q')
lsusb       #list usb devices
aplay -l    #list available soundcards
exit        #leave ssh
sudo halt -p
sudo reboot
sudo pkill pd
ls /dev/tty*    #see if /dev/ttyUSB0 is there
```

shutdown button
--

```python
import sys
from os import system
from time import sleep
import RPi.GPIO as GPIO
pinoff= 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinoff, GPIO.IN)
while True:
    if GPIO.input(pinoff)==0:
        system('sudo halt -p')
        sleep(10)
    sleep(0.5)
```
