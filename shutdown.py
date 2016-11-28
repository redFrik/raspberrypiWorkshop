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
