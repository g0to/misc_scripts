#! /bin/bash

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
# This peacock alarm will look after your laptop computer when you leave it   #
# alone.                                                                      #
#                                                                             #
# It will watch for the AC adapter plug. If the power cable is not plugged    #
# to your computer, the peacock will make your internal speaker beeping until #
# the cable is plugged in again or the program terminates.                    #
#                                                                             #
# Use it at your own risk when you are in the library or a quiet place and    #
# don't forget to finish the process once you come back to your laptop. You   #
# will not want to alarm people when disconnecting the computer power before  #
# going home ;)                                                               #
#                                                                             #
# REQUIRED PROGRAMS:                                                          #
#    - acpi								      #
#    - beep                                                                   #
#                                                                             #
#                                                                             #
#    by g0to                                                                  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" >&2
   exit 1
fi

FREQUENCY=9000
REPETITIONS=5

echo 
echo "            _/_"
echo "          -'a\ "
echo "            ||"
echo "            |J"
echo "            2_\ "
echo "           /:::\ "
echo "          |;ooo;|"
echo "          /Oo@ o\ "
echo "         '/o oOo\\\`"
echo "         /@ O o @\ "
echo "        '/.o,()o,\\\`"
echo "        /().O O  o\ "
echo "       / @ , @. () \ "
echo "      /,o O' o O o, \ "  
echo "   _-'. 'o _o _O_o-o.\`-_"
echo "   \`\"\"\"---......---\"\"\"\`"
echo
echo -n "  the peacock is looking after me..."

modprobe pcspkr
while :
do
    read -n1 -t1 -s OUT  # type any key to exit the program
    if [ -n "$OUT" ]
    then
        echo
        modprobe -r pcspkr
        exit 0
    elif [ "$(acpi -a | grep off-line)" ] 
    then 
	echo
        beep -f $FREQUENCY -r $REPETITIONS
        echo "WATCH OUT!!! The AC adapter was disconnected!"
    fi
done
