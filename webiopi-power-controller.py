#!/usr/bin/python
# Tyler Payne
# Inital webiopi configureation. Runs at webiopi service startup.

# Imports
import time
import webiopi

# Project Name
PROJECT_NAME = 'AC Controller'

# Alias GPIO library for convenience
GPIO = webiopi.GPIO

# Enable debug output
webiopi.setDebug()

# Set output and input pins
BUTTON = 17
POWER = 18


# A macro without args which return nothing
@webiopi.macro
def PrintTime():
    webiopi.debug("PrintTime: " + time.asctime())


@webiopi.macro
def printPower(pin=POWER):
    status = GPIO.digitalRead(pin)
    webiopi.debug(PROJECT_NAME + " - VAR = " + str(status))


@webiopi.macro
def togglePower(pin=POWER):
    if checkPowerState(pin):
        GPIO.digitalWrite(pin, False)
        webiopi.debug(PROJECT_NAME + " - Power Off")
    else:
        GPIO.digitalWrite(pin, True)
        webiopi.debug(PROJECT_NAME + " - Power On")


# turn the power off
@webiopi.macro
def powerOff(pin=POWER):
    GPIO.digitalWrite(pin, False)
    webiopi.debug(PROJECT_NAME + " - Power Off")


# turn the power on
@webiopi.macro
def powerOn(pin=POWER):
    GPIO.digitalWrite(pin, True)
    webiopi.debug(PROJECT_NAME + " - Power On")


# Returns True or False depending on current power state
# True - The power is currently on
# False - The power is currently off
def checkPowerState(pin=POWER):
    """Checks whether the device is in the on of off state."""
    status = GPIO.digitalRead(pin)
    webiopi.debug(PROJECT_NAME + " - Power is on?: " + str(status))
    return status


# Called by WebIOPi at script loading
def setup():
    webiopi.debug(PROJECT_NAME + " - Setup")

    #Setup GPIO
    GPIO.setFunction(BUTTON, GPIO.IN)
    GPIO.setFunction(POWER, GPIO.OUT)
    GPIO.digitalWrite(POWER, True)


# Looped by WebIOPi
def loop():
    webiopi.sleep(0.05)
    button_push = not GPIO.digitalRead(BUTTON)
    if button_push:
        togglePower()
        webiopi.sleep(0.5)
    webiopi.debug(PROJECT_NAME + " - " + str(button_push))


# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("AC Controller - Destroy")
    GPIO.setFunction(POWER, GPIO.IN)
    GPIO.setFunction(BUTTON, GPIO.IN)