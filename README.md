# raspberrypiWorkshop

held at [ems](http://elektronmusikstudion.se) 9oct2016, organized by [vems](https://vems.nu)

in this 3h workshop we will install the raspbian operating system from scratch, install [pure data](http://puredata.info) and [supercollider](http://supercollider.github.io) and last look at how to connect an [arduino](http://arduino.cc) board and send data to/from it and the raspberry pi.

**participants should bring:**

* laptop - preferably with sd card reader/writer
* micro sd card - 8gb or larger
* raspberry pi - model 1b, 2 or 3
* power supply - 5v micro usb for the rpi
* headphones with minijack
* ethernet cable
* arduino with usb cable

**additional:** (_but not necessary_)

* usb sound card
* usb wlan module
* breadboard, sensors, leds, wires

overview
==

these are the steps we will go through. it may look complicated but in practice there are only a few things one need to do. and after you've gone through it once, you should be able to perform it all again in <15min.

details are writting in _italic_.

1. [burn raspbian to your sd card](#burn-raspbian-to-your-sd-card)
2. [start your raspberry pi](#start-your-raspberry-pi)
3. [log in to your raspberry pi](#log-in-to-your-raspberry-pi)
4. [setup raspbian](#setup-raspbian)
5. [setup wifi](#setup wifi)
6. [install pure data](#install-pure-data)
7. [install supercollider](#install-supercollider)
8. [tune your audio](#tune-your-audio)
9. [autostart](#autostart)
10. [communicate with arduino](#communicate-with-arduino)
11. [useful terminal commands](#useful-terminal-commands)
12. [shutdown](#shutdown)

burn raspbian to your sd card
--

1. download the latest [raspbian image](https://www.raspberrypi.org/downloads/raspbian/)
    - _or copy the zip from the provided usbstick_
    -  _to save space you can use the .zip file directly without unpacking the .img_
    - _here we use 2016-09-23-raspbian-jessie - **not** the 'lite' version_
    - _jessie 'lite' will fit on a smaller sd card and is useful for non-gui audio-only headless systems_
2. download [etcher.io](http://etcher.io)
    - _works on osx, linux, windows_
    - _on osx you can also use [pifiller](http://ivanx.com/raspberrypi/)_
3. start etcher and select the raspbian zip file
4. insert your 8gb sd card
5. click flash
    - _on my machine the process takes ~9min_

![etcher](etcher.png)

start your raspberry pi
--

1. put the sd card in your raspberry pi
2. connect the ethernet cable to your raspberry pi
    - _the other end goes to your home wlan router or to your laptop_
    - _if you connect to a osx: go to system preferences / network and activate internet sharing - share from wifi to ethernet_
    - _if you connect to a windows machine: see [here](http://raspberrypi.stackexchange.com/questions/11684/how-can-i-connect-my-pi-directly-to-my-pc-and-share-the-internet-connection)_
3. connect 5v micro usb power supply
    - _always connect power last_
    - _and never pull the power without properly shutting down the system (see below)_
    - _on first boot the rpi will automatically expand the file system to make full use of the sd card_

log in to your raspberry pi
--

1. wait a bit after applying 5v
    - _specially on first boot it will take a while to connect to the network_
2. find your raspberry pi on the network and take note of the ip address (e.g. 192.168.1.52)
    - _we want to see that it is accessible and which ip address it got assigned_
    - _to find out you can log in to your router's admin setup panel_
    - _or on osx you can use [lanscan](https://www.iwaxx.com/lanscan)_
3. open a terminal window and type `ssh pi@192.168.1.52` (or )
    - _on osx terminal is found in your applications/utilities folder_
    - _on windows you can install [putty](?) and then see [here]()_
    - _if you get a warning about 'remote host identification' first do `ssh-keygen -R 192.168.1.52`_
    - _instead of the ip you can also use `ssh pi@raspberrypi` or `pi@raspberrypi.local`_
4. the default password 'raspberry'
5. make sure you can log in like in the picture below
6. then type `exit` to leave

![login](login.png)

setup raspbian
--

1. log in again using ssh
    - _via terminal or putty - see #3 above_
2. type `sudo raspi-config`
3. select change user password and enter a new password
4. select change hostname under advanced options and enter a new name
    - _this is so that you can identify your raspberry pi on the network_
    - _then use `ssh pi@mynewhostname` to log in_
5. optional: change memory split under advanced options
    - _if you run headless and never use gui you can set this to the lowest (16)_
    - _if you will do graphics (e.g. with openframeworks) set this to a higher value (256)_
6. optional: enable vnc under advanced options
    - _so that you can use the gui remotely with vnc viewer - see under setup wifi below_
    - _install real's [vnc viewer](https://www.realvnc.com/download/viewer/)_
7. finish and reboot

![raspiconfig](raspiconfig.png)

setup wifi
--

1. log again in via ssh
    - _note: use the new hostname and new password_
2. type `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
3. type or copy/paste the following at the bottom
      ```
      network={
          ssid="wifiname"
          psk="password"
      }
      ```
4. press ctrl+o to save and ctrl+x to exit
5. restart with `sudo reboot`
    - _the raspberry pi should now reboot and try to connect to the wifi network - check with lanscan or in your router's setup panel like before_
    - _if the raspberry pi could connect to wifi, you can now disconnect the ethernet cable_
6. optional: start real's vnc viewer and try to connect to your raspberry pi
    - _download it from [here](https://www.realvnc.com/download/viewer/)_
    - _make sure you have activated vnc in raspi-config - see above_

![wifi](wifi.png)

![vnc](vnc.png)

![desktop](desktop.png)

reference: [setting up wifi via command line](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)

install pure data
--

first make sure your raspberry is connected to the internet and then do the following.

1. `sudo apt-get update`
2. `sudo apt-get install puredata`
3. `apt-cache search "^pd-"` (this will just list libraries and externals)
4. `sudo apt-get install pd-comport pd-cyclone` (this will install two libraries that we need for arduino below)
5. `nano testsines.pd` and copy/paste in the following
    ```
    #N canvas 1068 88 450 300 10;
    #X obj 238 159 dac~;
    #X obj 235 73 osc~ 400;
    #X obj 289 73 osc~ 404;
    #X msg 126 154 \; pd dsp 1;
    #X obj 126 83 loadbang;
    #X obj 126 123 del 100;
    #X text 42 122 important ->;
    #X obj 238 111 *~ 0.2;
    #X obj 280 111 *~ 0.2;
    #X connect 1 0 7 0;
    #X connect 2 0 8 0;
    #X connect 4 0 5 0;
    #X connect 5 0 3 0;
    #X connect 7 0 0 0;
    #X connect 8 0 0 1;
    ```
6. `pd -stderr -nogui -verbose -audiodev 4 testsines.pd` (test different audiodev - 4 is usually the usb soundcard)

7. stop with ctrl+c
8. `nano testmic.pd` and copy/paste the following
#N canvas 1068 88 450 300 10;
#X obj 238 230 dac~;
#X msg 126 154 \; pd dsp 1;
#X obj 126 83 loadbang;
#X obj 126 123 del 100;
#X text 42 122 important ->;
#X obj 238 24 adc~;
#X obj 238 53 delwrite~ del1 500;
#X obj 238 123 delread~ del1 500;
#X obj 259 80 delwrite~ del2 750;
#X obj 280 144 delread~ del2 750;
#X obj 238 182 *~ 0.2;
#X obj 280 182 *~ 0.2;
#X connect 2 0 3 0;
#X connect 3 0 1 0;
#X connect 5 0 6 0;
#X connect 5 1 8 0;
#X connect 7 0 10 0;
#X connect 9 0 11 0;
#X connect 10 0 0 0;
#X connect 11 0 0 1;


reference: <http://www.fredrikolofsson.com/f0blog/?q=node/630>

install supercollider
--

reference: <https://github.com/redFrik/supercolliderStandaloneRPI2>

tune your audio
--

by default the alsa volume is quite low. it's recommended to turn it up so that you can lower the amplifier on the output and thereby get a less noisy signal.

```bash
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
ls              #list files
df -h           #disk free
free -h         #ram memory
top             #cpu usage (quit with 'q')
lsusb           #list usb devices
aplay -l        #list available soundcards
exit            #leave ssh
sudo halt -p    #turn off - wait for 10 blinks
sudo reboot     #restart
sudo pkill pd   #force quit on some program
ls /dev/tty*    #see if /dev/ttyUSB0 is there
```

shutdown
--

to safely turn off your raspberry pi you need to log in and type:

`sudo halt -p`

then wait for the led on the board to blink 10 times. now you can disconnect the 5v micro usb cable. if you don't power down the system in this way you risk corrupting the sd card.

another option is to add your own button to run a halt script when pressed. below is one way to do this using a python script that always run in the background.

1. log in and type `nano shutdown.py`
2. type or copy/paste the following
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
3. press ctrl+o to save and ctrl+x to exit
4. type `crontab -e` and add the following to the bottom
    `@reboot /usr/bin/python /home/pi/shutdown.py`
5. `sudo reboot`, wait for a bit and then connect a cable/button between gpio pin 3 and ground
