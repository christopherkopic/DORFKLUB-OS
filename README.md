# DORFKLUB-OS
This is the OS (aka large CircuitPython sketch) for my "DORFKLUB-MASCHINE" MIDI controller, which can be found [here.](https://github.com/christopherkopic/DORFKLUB-MASCHINE)


## Note
This is the current OS uploaded "as is", which means it's a mix of fairly neat, object oriented Python from when I was starting out and some spaghetti-codish bits from when I was quickly tacking on features at the end. 
I'm currently working on a refactored version of the code that will much more object oriented and will make it much easier to interface with the hardware on the pcb and build your own control schemes around it. This however will also change some of the controls around the encoder, so don't build too much muscle memory there.
Once this version is done, you'll be able to read about it here.

## Install Guide:
1. Download the Circuitpython uf2 file for your specific board here:
   https://circuitpython.org/downloads
2. Install it according to the instructions here:
   https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
3. Download the Adafruit CircuitPython library bundle here:
   https://circuitpython.org/libraries
4. Find the following files / folders in "lib" directory of the bundle and drag them into the "lib" folder on your Pico:
	1. adafruit_max7219 (folder)
	2. adafruit_midi (folder)
  3. adafruit_framebuf.mpy
  4. adafruit_simplemath.mpy
  5. keypad.mpy
  6. rotaryio.mpy
7. Drag all files from the v1-0 folder of this repo into the main folder on your Pico. Confirm to overwrite the "code.py" file.

## Usage:
The entire control scheme of this controller is built around the circle of fifths. By default the buttons are not mapped to your standard chromatic scale, but either a major or melodic minor scale in one of the keys on the circle of fifths. The upper row of buttons will play the same notes as the lower row, just on octave higher. Button 8 and 9 will always play the same note. There are button combos to move around the circle to quickly build chord progressions or change the key of your melody, without the need of memorizing scales.

| Button               | Effect                                                                                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Button 1-16          | Play notes (Velocity always at 127)                                                                                                                                                                                 |
| Left / Right         | Shift octave up or down                                                                                                                                                                                             |
| Alt                  | Quickly ramps a control change (channel XX) from 0 to 127 and vice versa, acting essentially like a knob. Used for building punch-in effects                                                                        |
| Poti 1-3             | Send control change (channels XX to XX)                                                                                                                                                                             |
| Encoder turning      | Move around the circle of fiths, selecting different keys                                                                                                                                                           |
| Encoder click        | Switch between the major and minor side of the circle of fiths. This will also map all notes on the keyboard to a major or minor scale.                                                                             |
| Encoder double-click | Switch between circle-of-fifth- and chromatic-scale-mode. In the latter mode, buttons 1-16 are mapped to your typical keyboard layout. All button combos related to the c.o.f. won't do anything in chromatic mode. |
| Shift + Button 1-16  | Change midi channel                                                                                                                                                                                                 |
| Shift + Left / Right | Same as encoder turning                                                                                                                                                                                             |
| Shift + Alt          | Same as encoder click                                                                                                                                                                                               |

## License

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a></p>

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/christopherkopic/DORFKLUB-OS">DORFKLUB-OS</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/christopherkopic">Christopher Kopic</a> is licensed under <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0
