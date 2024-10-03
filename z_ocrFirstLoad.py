import easyocr
from time import sleep

reader = None

print("Iniciar este file si es la primera vez...")
sleep(2)
reader = easyocr.Reader(['en'], gpu=False)
print("CARGADOOOOOOOOOOOOOOO")