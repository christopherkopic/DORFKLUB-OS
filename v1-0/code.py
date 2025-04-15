import board

from harmonizer import Harmonizer
from keyboard import Keyboard
from encoder import Encoder
from matrix import Matrix
from poti import Poti

matrix = Matrix()
harmonizer = Harmonizer(matrix)
keyboard = Keyboard(harmonizer)
encoder = Encoder(harmonizer)

tmpPorts = [board.A0, board.A1, board.A2]
tmpCC = [20,21,22]
potis = []
for i in range(3):
    potis.append(Poti(tmpPorts[i], tmpCC[i], harmonizer))

matrix.startupAnim()

while(True):
    keyboard.update()
    matrix.update()
    encoder.update()
    for poti in potis:
        poti.update()
    harmonizer.update()