from login import login_main
from menuTrainers import *
from menuCampers import *
from menuAdmin import *
from reportes import *
from menuGrupos import *
from utils import limpiar_pantalla

if __name__ == "__main__":
    try:
        limpiar_pantalla(pausa=1)
        login_main()
        print("logre que se ejecutara directo desde reportes.py pero solo si se inicia desde la consola alli mismo")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        input("Presiona ENTER para salir...")