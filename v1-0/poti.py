import board
import time
from analogio import AnalogIn

class Poti(object):
    def __init__(self, port, ccVal, harmonizer):
        self.harmonizer = harmonizer
        self.ccVal = ccVal

        self.poti = AnalogIn(port)
        self.value = self.poti.value
        self.lowpass = 0.8

        self.buffer = []
        for i in range(10):
            self.buffer.append(127 - self.value/512)
        self.lastBuffer = 0
        self.bufferTimeout = 0.03

        self.turning = False
        self.lastTurn = 0.0
        self.turningTimeout = 1.5

        self.turningPrev = False

    def lerp(self, a, b, alpha):
        return a * (1-alpha) + b * alpha
    
    def getMidiVal(self):
        self.value = self.lerp(self.poti.value, self.value, self.lowpass)
        return 127 - int(self.value/512)

    def checkTurning(self, val):
        # run rolling buffer of x entries
        if time.monotonic() - self.lastBuffer > self.bufferTimeout:
            self.buffer.pop(0)
            self.buffer.append(val)
            self.lastBuffer = time.monotonic()

        # calc difference from entry to entry
        lastEntry = self.buffer[0]
        accum = 0
        for entry in self.buffer:
            accum += entry - lastEntry
            lastEntry = entry

        # if abs differences bigger y - turning True, else False 
        if abs(accum) > 2:
            self.turning = True
            self.lastTurn = time.monotonic()
        elif time.monotonic() - self.lastTurn > self.turningTimeout:
            self.turning = False

    def update(self):
        midiValue = self.getMidiVal()

        self.checkTurning(midiValue)

        if self.turning:
            if self.turning != self.turningPrev:
                self.harmonizer.controlChangeStart(self.ccVal)

            self.harmonizer.controlChange(self.ccVal, midiValue)

        self.turningPrev = self.turning