import board
import time
from rotaryio import IncrementalEncoder
from digitalio import DigitalInOut, Direction

from harmonizer import Harmonizer

class Encoder(object):
    def __init__(self, harmonizer):
        self.harmonizer = harmonizer

        self.encoder = IncrementalEncoder(board.GP14, board.GP15)
        self.lastPosition = 0

        self.button = DigitalInOut(board.GP20)
        self.button.direction = Direction.INPUT
        self.lastRead = False
        self.clicked = False
        self.released = False

        self.lastclick = 0.0
        self.doubleClickTimeout = 0.5

    def update(self):
        position = self.encoder.position
        delta = position - self.lastPosition
        self.lastPosition = position

        if delta != 0 and not self.harmonizer.chromatic:
            self.harmonizer.changeKey(delta)

        read = not self.button.value
        if read != self.lastRead:
            if read == True:
                self.clicked = True
            else:
                self.released = True
        else:
            self.clicked = False
            self.released = False
        self.lastRead = read

        if self.clicked:
            if not self.harmonizer.chromatic:
                self.harmonizer.changeMinor()

            if time.monotonic() - self.lastclick < self.doubleClickTimeout:
                self.harmonizer.changeChromatic()

            self.lastclick = time.monotonic()
