#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                     #
#  SYNOPSIS                                                           #
#                                                                     #
#       m3u_generator [[-r] DIRECTORY]                                #
#                                                                     #
#  OPTIONS                                                            #
#                                                                     #
#       -r    find for mp3 files inside DIRECTORY, creating           #
#             appropiate m3u file, and all its subdirectories         #
#                                                                     #
#       NOTE: if no arguments are provided, "-r current directory"    #
#             will be default options                                 #
#                                                                     #
#  DESCRIPTION                                                        #
#                                                                     #
#       This script generates a m3u file containing the names of      #
#       the mp3 files inside a given directory (and subdirectories    #
#       if '-r' is provided).                                         #
#                                                                     #
#       Generated m3u file will have the same name as the directory   #
#       that contains it.                                             #
#                                                                     #
#       Both, one-only folder and recursive options, will not create  #
#       any m3u file if directory doesn't contain any mp3 files.      #
#                                                                     #
#                                                                     #
#   by g0to                                                           #
#                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import glob
import os
import sys

def generate_m3u(dir):
    mp3_files = glob.glob(os.path.join(dir, "*.mp3"))
    if mp3_files:  # go ahead only if dir contains any mp3 files
        f = open(os.path.join(dir, os.path.basename(dir)) + ".m3u", "w")
        for file in mp3_files:
            f.write(os.path.basename(file) + "\n")
        f.close()


if len(sys.argv) < 4:
    if len(sys.argv) == 2:
        generate_m3u(sys.argv[1])
        sys.exit(0)
        
    if len(sys.argv) == 1:
        target_dir = os.getcwd()
    elif len(sys.argv) == 3 and sys.argv[1] == "-r":
        target_dir = sys.argv[2]
    else:
        print "usage: %s [-r] <target_dir>" % sys.argv[0]
        sys.exit(0)
    
    generate_m3u(target_dir)
    for root, dirs, files in os.walk(target_dir):
        for dir in dirs:
            generate_m3u(os.path.join(root, dir))
    
else:
    print "usage: %s [-r] <target_dir>" % sys.argv[0]
