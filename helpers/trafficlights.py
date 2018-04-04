#!/usr/bin/env python3

class Colours(object):
    """docstring for TrafficLightColours"""

    def __init__(self):
        self.red="RED"
        self.green="GREEN"
        self.amber="AMBER"

    def RED(self):
        return self.red

    def AMBER(self):
        return self.amber

    def GREEN(self):
        return self.green


    def ALL(self):
        return [self.red, self.amber, self.green]
