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


# Returns True or False depending on current power state
# True - The power is currently on
# False - The power is currently off
def checkPowerState(pin):
    """Checks whether the device is in the on of off state."""
    if GPIO.digitalRead(pin, 0):
        return False
    else:
        return True

# A macro without args which return nothing
@webiopi.macro
def PrintTime():
    webiopi.debug("PrintTime: " + time.asctime())


@webiopi.macro
def letThereBeLight():
    GPIO.digitalWrite(POWER, True)


@webiopi.macro
def togglePower(pin=POWER):
    if checkPowerState(pin):
        GPIO.digitalWrite(pin, False)
        webiopi.debug(PROJECT_NAME + " - Power Off")
    else:
        GPIO.digitalWrite(pin, True)
        webiopi.debug(PROJECT_NAME + " - Power On")


# Called by WebIOPi at script loading
def setup():
    webiopi.debug(PROJECT_NAME + " - Setup")

    #Setup GPIO
    GPIO.setFunction(BUTTON, GPIO.IN)
    GPIO.setFunction(POWER, GPIO.OUT)
    GPIO.digitalWrite(POWER, True)


# Looped by WebIOPi
def loop():
    # Toggle power state with button.
    time.sleep(0.1)
    if GPIO.digitalRead(BUTTON):
        togglePower(POWER)


# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("AC Controller - Destroy")
    GPIO.setFunction(POWER, GPIO.IN)
    GPIO.setFunction(BUTTON, GPIO.IN)