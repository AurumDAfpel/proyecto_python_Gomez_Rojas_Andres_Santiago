import os
import platform
import time

def limpiar_pantalla(pausa=0):
    
    sistema = platform.system() 

    if pausa > 0:
        time.sleep(pausa)
        
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")
