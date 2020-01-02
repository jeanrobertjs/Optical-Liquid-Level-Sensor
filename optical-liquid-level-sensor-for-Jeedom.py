#!/usr/bin/python
#
# optical-liquid-level-sensor-for-Jeedom.py
# Measure state of an optical liquid level sensor in a loop for Jeedom (a home automation server)
# 
# Optical Liquid Level sensor related post: https://github.com/jeanrobertjs/Optical-Liquid-Level-Sensor/
# 
# Author : Jean-Robert JEAN-SIMON
# Date   : 02/01/2020
# -----------------------

#########
# About #
#########
# This script uses Raspberry Pi GPIOs with an optical liquid level sensor to sense for the presense or absense of water
# and sends the value via an HTTP request to a Jeedom server and a virtual equipment in 'Virtual' Jeedom plugin.
# If there is water, the LED and a buzzer go on.
# When it's dry again, the LED and the buzzer turn off.

# To run this script at boot, edit /etc/rc.local to include (no quotes) 'sudo python <pathtoyourscript>.py'

####################################
# Import required Python libraries #
####################################
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

# Define GPIO to use on Raspberry Pi
GPIO_OPTICAL_LIQUID_LEVEL_SENSOR  = 5
GPIO_BUZZER                       = 6

# Wrap main content in a try block so we can catch the user pressing CTRL-C and run the GPIO cleanup function.
# This will also prevent the user seeing lots of unnecessary error messages.
try:
    print "Optical liquid level measurement"
    print "Waiting for wetness..."
    while True:
        isWet = optical_liquid_level_state(GPIO_OPTICAL_LIQUID_LEVEL_SENSOR)
        if isWet == 0:
            print "Sensor is Dry."
            buzz_off(GPIO_BUZZER)
        if isWet == 1:
            print "Sensor is Wet."
            buzz_on(GPIO_BUZZER)
        payload = {'plugin': 'virtual', 'apikey': 'APIKEYDEJEEDOM' , 'type': 'virtual' , 'id': 'IDDUVIRTUAL' , 'value': isWet}
        r = requests.post("http://JEEDOMSERVERURL/core/api/jeeApi.php", params=payload)
        time.sleep(1)

except KeyboardInterrupt:
    # User pressed CTRL-C
    # Reset GPIO settings
    GPIO.cleanup()