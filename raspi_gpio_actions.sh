#! /bin/bash

 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
#                                                                             #     
# This script configures which GPIO pins of the Raspberry Pi will be          #
# available and in which direction (read or write). It also takes some        #
# actions if someone interacts with the selected pins.                        #
#                                                                             #
# More info about the GPIO: http://elinux.org/RPi_Low-level_peripherals       #
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
#                                                                             #
#  by g0to                                                                    #
#                                                                             #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  


if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" >&2
   exit 1
fi

SHUTDOWN_PIN="3"
#DHCP_ON_PIN="2"

echo "$SHUTDOWN_PIN" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio"$SHUTDOWN_PIN"/direction
#echo "$DHCP_ON_PIN" > /sys/class/gpio/export
#echo "in" > /sys/class/gpio/gpio"$DHCP_ON_PIN"/direction

while ( true )
do
    # check if the pin is connected to GND and, if so, halt the system
    if [ $(</sys/class/gpio/gpio"$SHUTDOWN_PIN"/value) == 0 ]
    then
        echo "$SHUTDOWN_PIN" > /sys/class/gpio/unexport
        shutdown -h now "System halted by a GPIO action"
#   elif [ $(</sys/class/gpio/gpio"$DHCP_ON_PIN"/value) == 0 ]
#   then
#       dhclient eth0
    fi
    
    sleep 60
done
