import serial
import numpy as np
from PIL import Image

PORT = "/dev/ttyACM0"
BAUD = 115200

WIDTH = 160
HEIGHT = 120
FRAME_SIZE = WIDTH * HEIGHT

ser = serial.Serial(PORT, BAUD, timeout=10)

print("Esperando frames...")

while True:
    # espera o marcador "FRAME"
    line = ser.readline()
    if not line:
        continue
    if not line.startswith(b"FRAME"):
        continue

    # lê o frame completo
    buf = bytearray()
    while len(buf) < FRAME_SIZE:
        chunk = ser.read(FRAME_SIZE - len(buf))
        if not chunk:
            break
        buf.extend(chunk)

    if len(buf) < FRAME_SIZE:
        print(f"Frame incompleto: recebi {len(buf)} bytes")
        continue

    # converte em imagem 
    img_array = np.frombuffer(buf, dtype=np.uint8).reshape((HEIGHT, WIDTH))
    img = Image.fromarray(img_array, mode="L")

    # mostra a imagem (abre numa janela separada)
    img.show()

    # salva em arquivo (sobrescreve sempre)
    img.save("frame.jpg")
    print("Frame salvo")
