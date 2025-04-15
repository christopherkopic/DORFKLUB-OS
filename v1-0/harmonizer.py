import usb_midi
import time
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange
from adafruit_simplemath import map_range

import icons

class Harmonizer(object):
    def __init__(self, matrix):
        self.matrix = matrix

        # Constants
        self.cofMajor = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
        self.cofMinor = [9, 4, 11, 6, 1, 8, 3, 10, 5, 0, 7, 2]

        self.majorStep = [0,2,4,5,7,9,11,12, 12,14,16,17,19,21,23,24]
        self.melMinorStep = [0,2,3,5,7,9,11,12, 12,14,15,17,19,21,23,24]
        self.chromaticStep = [0,2,4,5,7,9,11,12, 1,1,3,6,6,8,10,13]

        self.btnChannelMapping = [8,9,10,11,12,13,14,15, 0,1,2,3,4,5,6,7]

        self.punchInDuration = 0.15

        # Global Variables
        self.lastNotes = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        self.octave = 4
        self.key = 0
        self.minor = False
        self.chromatic = False
        self.activeKnob = -1

        self.punching = False
        self.punchForward = True
        self.lastPunch = 0
        self.punchDuration = 0
        self.punchPos = 0
        self.punchStart = 0

        # Setup
        self.midi = MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        #self.midiPunch = MIDI(midi_out=usb_midi.ports[1], out_channel=15)

    def noteStart(self, btn):
        outNote = 0
        if self.chromatic:
            outNote = self.octave*12 + self.chromaticStep[btn]
        elif self.minor:
            outNote = self.cofMinor[self.key] + self.octave*12 + self.melMinorStep[btn]
        else:
            outNote = self.cofMajor[self.key] + self.octave*12 + self.majorStep[btn]
        outNote = self.constrain(outNote, 0, 127)

        self.lastNotes[btn] = outNote
        self.midi.send(NoteOn(outNote, 127))

    def noteEnd(self, btn):
        outNote = self.lastNotes[btn]
        if outNote != -1:
            self.lastNotes[btn] = -1
            self.midi.send(NoteOff(outNote, 127))

    def punchInStart(self):
        #self.midiPunch.send(NoteOn(48, 127))
        self.activeKnob = -1
        self.matrix.displayImg(icons.punch)

        self.punching = True
        self.punchForward = True
        self.lastPunch = time.monotonic()
        self.punchStart = self.punchPos
        self.punchDuration = map_range(self.punchStart, 0, 127, self.punchInDuration, 0.0)

    def punchInEnd(self):
        #self.midiPunch.send(NoteOff(48, 127))

        self.punching = True
        self.punchForward = False
        self.lastPunch = time.monotonic()
        self.punchStart = self.punchPos
        self.punchDuration = map_range(self.punchStart, 127, 0, self.punchInDuration, 0.0)

    def punchInUpdate(self):
        currentTime = time.monotonic()
        if currentTime - self.lastPunch > self.punchDuration:
            self.punching = False
            if self.punchForward:
                self.midi.send(ControlChange(23, 127))
            else:
                self.midi.send(ControlChange(23, 0))

            return
        
        goal = 0
        if self.punchForward:
            goal = 127

        value = int(map_range(currentTime,
                            self.lastPunch,
                            self.lastPunch + self.punchDuration,
                            self.punchStart,
                            goal))

        self.midi.send(ControlChange(23, value))
        self.punchPos = value

    def controlChangeStart(self, id):
        self.activeKnob = id

    def controlChange(self, control, value):
        self.midi.send(ControlChange(control, value))

        if control == self.activeKnob:
            self.matrix.displayBar(value/2)

    def updateAll(self):
        for btn in range(16):
            note = self.lastNotes[btn]
            if note != -1:
                self.noteEnd(btn)
                self.noteStart(btn)

    def changeOctave(self, step):
        self.activeKnob = -1

        self.octave = self.constrain(self.octave + step, 0, 7)
        self.matrix.displayImg(icons.iconsOctaves[self.octave])
        self.updateAll()

    def changeKey(self, step):
        self.activeKnob = -1

        self.key = (self.key + step) % 12
        if self.minor:
            self.matrix.displayImg(icons.iconsCofMinor[self.key])
        else:
            self.matrix.displayImg(icons.iconsCofMajor[self.key])
        self.updateAll()

    def changeMinor(self):
        self.activeKnob = -1

        self.minor = not self.minor
        if self.minor:
            self.matrix.displayImg(icons.iconsCofMinor[self.key])
        else:
            self.matrix.displayImg(icons.iconsCofMajor[self.key])
        self.updateAll()

    def changeChromatic(self):
        self.activeKnob = -1

        self.chromatic = not self.chromatic
        if self.chromatic:
            self.matrix.displayImg(icons.chromatic)
        else:
            self.matrix.displayImg(icons.cof)
        self.updateAll()

    def changeChannel(self, btn):
        for button in range(16):
            self.noteEnd(button)

        channel = self.btnChannelMapping[btn]
        self.midi.out_channel = channel

        self.activeKnob = -1
        self.matrix.displayImg(icons.iconsChannel[channel])

    def constrain(self, val, low, high):
        if(val < low):
            val = low
        elif(val > high):
            val = high
        return val

    def update(self):
        if self.punching:
            self.punchInUpdate()