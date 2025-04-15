import board
from keypad import KeyMatrix, Event

from harmonizer import Harmonizer

class Keyboard(object):
    def __init__(self, harmonizer):
        self.harmonizer = harmonizer

        self.km = KeyMatrix(
            row_pins=(board.GP3, board.GP2),
            column_pins=(board.GP13, board.GP12, board.GP11, board.GP10, board.GP9, board.GP8, board.GP7, board.GP6, board.GP5, board.GP4)
        )

        tmpSpecial = {
            "Left":0,
            "Right":1,
            "Alt":10,
            "Shift":11
        }
        self.eSpecialOn = {}
        self.eSpecialOff = {}
        for key, index in tmpSpecial.items():
            self.eSpecialOn.update({key:Event(index, True)})
            self.eSpecialOff.update({key:Event(index, False)})

        tmpKeys = [12,13,14,15,16,17,18,19,2,3,4,5,6,7,8,9]
        self.eKeysOn = []
        self.eKeysOff = []
        for key in tmpKeys:
            self.eKeysOn.append(Event(key, True))
            self.eKeysOff.append(Event(key, False))

        self.isShifted = False

    def update(self):
        event = self.km.events.get()
        
        if not event:
            return
        
        if event == self.eSpecialOn["Shift"]:
            self.isShifted = True

        if event == self.eSpecialOff["Shift"]:
            self.isShifted = False

        if event == self.eSpecialOn["Left"]:
            if not self.isShifted:
                self.harmonizer.changeOctave(-1)
            else:
                self.harmonizer.changeKey(-1)

        if event == self.eSpecialOn["Right"]:
            if not self.isShifted:
                self.harmonizer.changeOctave(1)
            else:
                self.harmonizer.changeKey(1)

        if event == self.eSpecialOn["Alt"]:
            if not self.isShifted:
                self.harmonizer.punchInStart()
            else:
                self.harmonizer.changeMinor()

        if event == self.eSpecialOff["Alt"]:
            self.harmonizer.punchInEnd()

        for btn in range(16):
            if event == self.eKeysOn[btn]:
                if not self.isShifted:
                    self.harmonizer.noteStart(btn)
                else:
                    self.harmonizer.changeChannel(btn)
            if event == self.eKeysOff[btn]:
                self.harmonizer.noteEnd(btn)