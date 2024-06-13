import easyocr
import time

reader = None

print("Iniciar este file si es la primera vez...")
time.sleep(2)
reader = easyocr.Reader(['en'], gpu=False)
print("CARGADOOOOOOOOOOOOOOO")