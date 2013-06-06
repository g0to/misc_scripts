#! /usr/bin/env python 

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
#                                                                             #     
# This script configures which GPIO pins of the Raspberry Pi will be          #
# available and in which direction (read or write). It also takes some        #
# actions if someone interacts with the selected pins.                        #
#                                                                             #
# More info about the GPIO: http://elinux.org/RPi_Low-level_peripherals       #
#                                                                             #
# Info about this version of the script, which uses interruptions:            #
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio
#                                                                             #
# See the polling approach using bash scripting:                              #
# https://github.com/g0to/misc_scripts/blob/master/raspi_gpio_actions.sh      #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
# -Raspberry Pi Rev2. GPIO layout:                                            #
#                                                                             #
#           2  4  6  8  10 12 14 16 18 20 22 24 26    _R_C_A_                 #
#           |  |  |  |  |  |  |  |  |  |  |  |  |     |______|                #
#           --------------------------------------                            #
#           |  |  |  |  |  |  |  |  |  |  |  |  |                             #
#    _      1  3  5  7  9  11 13 15 17 19 21 23 25                            #
#   | |                                                                       #
#   | | SD Card                                                               #
#   | |                                                                       #
#   |_|                                                                       #
#                                                                             #
#   P1-01: 3.3v       P1-10: GPIO15     P1-20: GND                            #
#   P1-02: 5.0v       P1-11: GPIO17     P1-21: GPIO9                          #
#   P1-03: GPIO2      P1-12: GPIO18     P1-22: GPIO25                         #
#   P1-04: 5.0v       P1-13: GPIO27     P1-23: GPIO11                         #
#   P1-05: GPIO3      P1-14: GND        P1-24: GPIO8                          #
#   P1-06: GND        P1-15: GPIO22     P1-25: GND                            #
#   P1-07: GPIO4      P1-16: GPIO23     P1-26: GPIO7                          #
#   P1-08: GPIO14     P1-17: 3.3v                                             #
#   P1-09: GND        P1-18: GPIO24                                           #
#                     P1-19: GPIO10                                           #
#                                                                             #
# NOTE: Pins GPIO2 and GPIO3 have a 1K8 pull up resistor, which means that    # 
# you can short cirtuit them directly to ground and you'll get a 1 as a non   #
# connected value (iddle) and a 0 as a connected value (short circuit to GND) #
# when reading them.                                                          #
#                                                                             #
#  original script by Alex Eames                                              #  
#  modifications by g0to                                                      #
#                                                                             #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

import subprocess
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# GPIO3 (pin 5) set up as input. It is pulled up to stop false signals
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# wait for the pin to be sorted with GND and, if so, halt the system
GPIO.wait_for_edge(3, GPIO.FALLING)
subprocess.call(['shutdown -h now "System halted by GPIO action"'], shell=True)

# clean up GPIO on normal exit
GPIO.cleanup()           
