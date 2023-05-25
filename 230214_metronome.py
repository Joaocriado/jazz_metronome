#!/usr/bin/env python3
import os
import readline #history for input with arrows
import atexit #save history

from time import sleep
from subprocess import Popen


histfile = 'history'
try:
    readline.read_history_file(histfile)
    readline.set_history_length(25)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    
    #change outter values
    if value < leftMin:
        value = leftMin
    elif value > leftMax:
        value = leftMax

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)
    # invert range for tempo
    valueScaled = (valueScaled * (-1)) + 1

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def saisir():
    global formule_r, pauze0, pauze1, ratio

    try:
        saisie = input("tempo [r]hythm [b]ar : ")
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        quit()

    saisie = saisie.split(" ")
    bpm = float(saisie[0])
    pauze0 = 60/bpm
    pauze1 = pauze0

    try:
        if saisie[1][0] == "r":
            formule_r = saisie[1].replace('/', '')[1:]
            if saisie[1][1] == "8":
                formule_r = formule_r[1:]
                pauze0 = pauze0/2
                pauze1 = pauze1/2
            elif saisie[1][1] == "s":
                formule_r = formule_r[1:]
                swing_ratio = translate(bpm, 40, 300, 1.5, 2)               #ratio du swing entre 1,6 et 2 tiers selon le tempo, binarisation dans le up
                print("ratio du swing : " + str(f'{swing_ratio:.{2}f}'))
                pauze0 = pauze0*(swing_ratio/3)
                pauze1 = pauze1*((3 - swing_ratio)/3)
            elif saisie[1][1] == "3":
                formule_r = formule_r[1:]
                pauze0 = pauze0/3
                pauze1 = pauze1/3
        elif saisie[1][0] == "j":
            formule_r = "-.-."
        else:
            formule_r = "...."
        print(saisie[1][1:])
    except IndexError:
            formule_r = "...."

    try:
        if saisie[2][0] == "b":
            nb = saisie[2][1:]
            marquage = "*" + formule_r[1:]
            for item in range(1, int(nb)):     #hear bars
                marquage = marquage + formule_r
            formule_r = marquage
    except IndexError:
        pass

    play_clic()

def play_clic():
    swing_state = 0
    try:
        while True:
            for item in range(0, len(formule_r)):
                if formule_r[item] == ".":
                    Popen(["ogg123", "-q", "rimshot.ogg"])
                elif formule_r[item] == "*":
                    Popen(["ogg123", "-q", "cowbell.ogg"])
                elif formule_r[item] == "+":
                    Popen(["ogg123", "-q", "clave.ogg"])
                if swing_state==0:
                    sleep(pauze0)
                    swing_state = 1
                else:
                    sleep(pauze1)
                    swing_state = 0
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        saisir()


saisir()
