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

1. [burn raspbian to your sd card](burn raspbian to your sd card)

2. [start your raspberry pi](start your raspberry pi)

3. [log in to your raspberry pi](log in to your raspberry pi)

4. [installing pure data](installing pure data)

5. [installing supercollider](installing supercollider)

6. [tune your audio](tune your audio)

7. [autostart](autostart)

8. [communicate with arduino](communicate with arduino)

9. [useful terminal commands](useful terminal commands)

10. [shutdown button](shutdown button)

burn raspbian to your sd card
--

* sd card (_must be 8gb or larger_)
* laptop (_or other computer with sd reader/writer_)
* [etcher.io](http://etcher.io) (_mac, linux, windows_)
* latest raspbian image - here [2016-05-27-raspbian-jessie.img](https://www.raspberrypi.org/downloads/raspbian/) (_you can use the .img file or better just burn the .zip file without unpacking_)

start your raspberry pi
--

* 5v micro usb (_for power_)
* ethernet cable (_connect to your home router or directly to laptop - activate internet sharing - change wlan on the rpi_)
* raspberry pi (_insert the sd card before connecting 5v power_)
* on first boot the rpi will automatically expand the file system

log in to your raspberry pi
--

* wait a bit
* find it on the network
log in to router
use lanscan
ssh pi@raspberry
ssh-keygen -R raspberrypi
default password 'raspberry'
sudo raspi-config
#change user password
#advanced options / hostname
#advanced options / memory split
#advanced options / vnc
'exit' to leave

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
