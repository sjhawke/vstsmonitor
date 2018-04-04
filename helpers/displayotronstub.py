#!/usr/bin/env python3


class Display:
    def __init__(self, colours):
        self.colours = colours

    def setcolour(self, colour):
        print(":::set screen colour > " + str(colour))

    def settext(self, text):
        line = "::: set screen text > " + text
        print (line)

    def setbarlevel(self, percent):
        print(":::Setting bar at > " + str(percent) + "% ")

    def clear(self):
        print("::: set screen clear")
