import board
import time
from digitalio import DigitalInOut
from busio import SPI
from adafruit_max7219.matrices import CustomMatrix

import icons

class Matrix(object):
    def __init__(self):
        spi = SPI(board.GP18, board.GP19, board.GP16)
        cs = DigitalInOut(board.GP17)
        self.matrix = CustomMatrix(spi, cs, 8, 8)
        self.matrix.brightness(1)

        self.displaying = False
        self.lastDisplay = 0
        self.displayTimeout = 0.75

    def startupAnim(self):
        for frame in icons.iconsAnim:
            self.displayImg(frame)
            time.sleep(0.04)

    def displayClear(self):
        self.matrix.fill(False)
        self.matrix.show()

        self.displaying = False

    def displayImg(self, img):
        self.matrix.fill(False)
        for y in range(8):
            for x in range(8):
                self.matrix.pixel(x,y,img[7-y][7-x])
        self.matrix.show()

        self.displaying = True
        self.lastDisplay = time.monotonic()

    def displayBar(self, value):
        self.matrix.fill(False)
        matrixpos = 0
        for y in range(8):
            for x in range(8):
                if matrixpos > value:
                    break

                if not y % 2:
                    self.matrix.pixel(x, y, 1)
                else:
                    self.matrix.pixel(7 - x, y, 1)
                matrixpos += 1
        self.matrix.show()

        self.displaying = True
        self.lastDisplay = time.monotonic()

    def update(self):
        if self.displaying and time.monotonic() - self.lastDisplay > self.displayTimeout:
            self.displayClear()