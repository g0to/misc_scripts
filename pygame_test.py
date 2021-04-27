#!/usr/bin/env python

import pygame


pygame.init()
dual_chock = pygame.joystick.Joystick(0)

while True:
    event = pygame.event.wait()
    if event.type == pygame.JOYHATMOTION and\
       event.hat == 0:
        if event.value == (-1,0):
            print("left")
        elif event.value == (1,0):
            print("right")
        elif event.value == (0,1):
            print("up")
        elif event.value == (0,-1):
            print("down")
    elif event.type == pygame.JOYBUTTONDOWN:
        print(event.button)
        if event.button == 12:
            # PS button
            break

print("byeeeee")
pygame.joystick.quit()
