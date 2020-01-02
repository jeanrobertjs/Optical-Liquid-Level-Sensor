#!/usr/bin/python
#
# optical-liquid-level-sensor.py
# Measure state of an optical liquid level sensor in a loop.
# 
# Optical Liquid Level sensor related post: https://github.com/jeanrobertjs/Optical-Liquid-Level-Sensor/
# 
# Author : Jean-Robert JEAN-SIMON
# Date   : 02/01/2020
# -----------------------

#########
# About #
#########
# This script uses Raspberry Pi GPIOs with an optical liquid level sensor to sense for the presense or absense of water.
# If there is water, an email is sent and a buzzer goes off.
# When it's dry again, another email is sent, and the buzzer turns off.

# To run this script at boot, edit /etc/rc.local to include (no quotes) 'sudo python <pathtoyourscript>.py'

import RPi.GPIO as GPIO
import time
import requests
import string

########################
# Function Definitions #
########################

# Tests whether water is present.
## Returns 0 for dry
## Returns 1 for wet
def optical_liquid_level_state (pin):
    reading = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1) 
    GPIO.setup(pin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while True:
        if (GPIO.input(pin) == GPIO.LOW):
            reading += 1
        if reading >= 1000:
            return 0
        if (GPIO.input(pin) != GPIO.LOW):
            return 1

# Turns on the piezo buzzer 
def buzz_on (pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Turns off the piezo buzzer
def buzz_off(pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


#############
# Main Loop #
#############
# Wrap main content in a try block so we can catch the user pressing CTRL-C and run the GPIO cleanup function.
# This will also prevent the user seeing lots of unnecessary error messages.

try:
    print 'Waiting for wetness...'
    while True:
        isWet = optical_liquid_level_state(5)
        if isWet == 0:
            buzz_off(6)
            print "Sensor is Dry."
        if isWet == 1:
            print "Sensor is Wet."
            buzz_on(6)
        time.sleep(1)

except KeyboardInterrupt:
    # User pressed CTRL-C
    # Reset GPIO settings
    GPIO.cleanup()