#!/usr/bin/env python3

import time

import dothat.backlight as backlight
import dothat.lcd as lcd


class Display:
    DEFAULT_CONTRAST = 50  # VALID RANGE => 0-63

    def __init__(self, colours, backlight=backlight, lcd=lcd):
        self.backlight = backlight
        self.lcd = lcd
        self.colours = colours
        self.backlight.rgb(0, 0, 0)
        self.backlight.set_graph(0.0)
        self.lcd.set_contrast(self.DEFAULT_CONTRAST)

    def setcolour(self, colour):
        if colour == self.colours.GREEN():
            self.backlight.rgb(0, 255, 0)
        elif colour == self.colours.RED():
            self.backlight.rgb(255, 0, 0)
        elif colour == self.colours.AMBER():
            self.backlight.sweep(0.5, 0.1)
            self.backlight.rgb(255, 255, 0)

    def settext(self, text):
        self.lcd.clear()
        time.sleep(0.2)
        self.lcd.write(text)
        # line = ":::" + text
        # print (line)

    def setbarlevel(self, percent):
        print("Setting bar at : " + str(percent) + "% ")
        self.backlight.set_graph(percent / 6.0)

    def clear(self):
        self.backlight.rgb(0, 0, 0)
        self.lcd.clear()
        self.backlight.set_graph(0.0)
