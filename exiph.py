#!/usr/bin/env python
# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                     #
#  SYNOPSIS                                                           #
#                                                                     #
#       exiph [[-r] DIRECTORY]                                        #
#                                                                     #
#  OPTIONS                                                            #
#                                                                     #
#       -r    find for jpg files inside DIRECTORY, renaming           #
#             them, and all its subdirectories                        #
#                                                                     #
#       NOTE: if no arguments are provided, "-r current directory"    #
#             will be default options                                 #
#                                                                     #
#  DESCRIPTION                                                        #
#                                                                     #
#     This script renames all jpg files inside a given directory      #
#     using its EXIF metadata. The resulting name will be the date    #
#     and time stored in the proper EXIF tag and formatted as:        #
#                                                                     #        
#                yyyy_mm_dd-hh_MM_ss_xx                               #
#                                                                     #
#               yyyy: four digits year                                #
#               mm: two digits month                                  #
#               dd: two digits day                                    #
#               hh: hour (24h format)                                 #
#               MM: minutes                                           #
#               ss: seconds                                           #
#               xx: two digits counter for images taken in the same   #
#                   second                                            #
#                                                                     #
#     If the image doesn't contain any or valid EXIF information      #
#     file won't be renamed                                           #
#                                                                     #
#                                                                     #
#  by g0to                                                            #
#                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import glob
import os
import sys
from PIL import Image

def resolve_duplicate(path):
    counter = 1
    suffix = "%02d" % counter 

    while os.path.exists(os.path.splitext(path)[0][:-3] + '_' + suffix + ".jpg"):
        counter += 1
        suffix = "%02d" % counter 
    
    return (os.path.splitext(path)[0][:-3] + '_' + suffix + ".jpg")

def rename_images(dir):
    image_paths = glob.glob(os.path.join(dir, "*.[Jj][Pp][Gg]"))
    for image_path in image_paths:
        exif_data = Image.open(image_path)._getexif()
        try:
            new_name = exif_data[36867].replace(':','_').replace(' ','-') # 36867 is the EXIF Date_Time tag number
                                                                          # file name format yyyy_mm_dd-hh_MM_ss
            new_name = new_name.rstrip('\0')  # removes trailing NULL space if any
        except (TypeError, KeyError):
            continue
        new_path = os.path.join(os.path.dirname(image_path), new_name + "_00.jpg")
        if os.path.exists(new_path):
            new_path = resolve_duplicate(new_path)
        os.rename(image_path, new_path) 
        ## debug 
        ## print image_path + " -> " + new_path

if len(sys.argv) < 4:
    if len(sys.argv) == 2:
        rename_images(sys.argv[1])
        sys.exit(0)
        
    if len(sys.argv) == 1:
        target_dir = os.getcwd()
    elif len(sys.argv) == 3 and sys.argv[1] == "-r":
        target_dir = sys.argv[2]
    else:
        print "usage: %s [-r] <target_dir>" % sys.argv[0]
        sys.exit(0)
    
    rename_images(target_dir)
    for root, dirs, files in os.walk(target_dir):
        for dir in dirs:
            rename_images(os.path.join(root, dir))
    
else:
    print "usage: %s [-r] <target_dir>" % sys.argv[0]
