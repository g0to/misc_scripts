#! /bin/bash

#  #  #  #  # 
# 
# Use it to backup a full system (/*) for later easy restore.
#
# Script source: https://wiki.archlinux.org/index.php/Full_System_Backup_with_rsync
# For detailed explanation about used arguments, see the man and the link above ;)
#
#  #  #  #  # 

if [[ $EUID -ne 0 ]]; then
   echo "$0 must be run as root" >&2
   exit 1
fi

if [ $# -lt 1 ]; then 
    echo "No destination defined. Usage: $0 destination" >&2
    exit 1
elif [ $# -gt 1 ]; then
    echo "Too many arguments. Usage: $0 destination" >&2
    exit 1
fi

invoke-rc.d deluge-web stop
invoke-rc.d deluge-daemon stop

START=$(date +%s)
rsync -aAXvh /* $1 --exclude={/dev/*,/proc/*,/sys/*,/tmp/*,/run/*,/mnt/*,/media/*,/lost+found}
FINISH=$(date +%s)
echo "total time: $(( ($FINISH-$START) / 60 )) minutes, $(( ($FINISH-$START) % 60 )) seconds"

invoke-rc.d deluge-daemon start
invoke-rc.d deluge-web start

echo "Backup performed on $(date '+%A, %d %B %Y, %T')"
