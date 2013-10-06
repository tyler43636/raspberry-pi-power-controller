#!/usr/bin/env python
# Tyler Payne
# Initial webiopi configuration. Runs at webiopi service startup.

import time
import webiopi

# Project Name
PROJECT_NAME = 'Power Controller'

# Alias GPIO library for convenience
GPIO = webiopi.GPIO

# Enable debug output
webiopi.setDebug()

# Set output and input pins
BUTTON = 17
POWER = 18


@webiopi.macro
def powerStatus(pin=POWER):
    """ returns 'True' if the power is on 'False' is it is off."""
    status = GPIO.digitalRead(pin)
    webiopi.debug(PROJECT_NAME + " - VAR = " + str(status))
    return status


@webiopi.macro
def togglePower(pin=POWER):
    """ toggle the power state"""
    if checkPowerState(pin):
        GPIO.digitalWrite(pin, False)
        webiopi.debug(PROJECT_NAME + " - Power Off")
    else:
        GPIO.digitalWrite(pin, True)
        webiopi.debug(PROJECT_NAME + " - Power On")


@webiopi.macro
def powerOff(pin=POWER):
    """ Turns the power off """
    GPIO.digitalWrite(pin, False)
    webiopi.debug(PROJECT_NAME + " - Power Off")


@webiopi.macro
def powerOn(pin=POWER):
    """ Turns the power on"""
    GPIO.digitalWrite(pin, True)
    webiopi.debug(PROJECT_NAME + " - Power On")


def checkPowerState(pin=POWER):
    """
        Checks whether the device is in the on of off state.
        True - The power is currently on
        False - The power is currently off
    """
    status = GPIO.digitalRead(pin)
    webiopi.debug(PROJECT_NAME + " - Power Status | On=" + str(status))
    return status


def setup():
    """ Called when webiopi starts """
    webiopi.debug(PROJECT_NAME + " - Setup")

    #Setup GPIO
    GPIO.setFunction(BUTTON, GPIO.IN)
    GPIO.setFunction(POWER, GPIO.OUT)
    GPIO.digitalWrite(POWER, True)


def loop():
    """ Loop run by WebIOPi """
    webiopi.sleep(0.05)
    button_push = not GPIO.digitalRead(BUTTON)
    if button_push:
        togglePower()
        webiopi.sleep(0.5)


def destroy():
    """ Called by WebIOPi at server exit """
    webiopi.debug("AC Controller - Destroy")
    GPIO.setFunction(POWER, GPIO.IN)
    GPIO.setFunction(BUTTON, GPIO.IN)