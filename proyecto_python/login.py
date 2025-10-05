import json
import os
from menuAdmin import menuAdmin
from menuCampers import menuCampers
from menuTrainers import menuTrainers
from utils import limpiar_pantalla

ruta_archivo_admin = os.path.join(os.path.dirname(__file__), "credenciales.json")

def login():

    print("""bienvenido a la base de datos de campus
        
    deseas iniciar sesion?(s/n)
        
    """)

    opcion = input().lower().strip()
    return opcion

def validarSesion(nombre, password):
    try:
        with open(ruta_archivo_admin, "r") as f:
            usuarios = json.load(f)
            for usuario in usuarios:
                if usuario["nombre"] == nombre and usuario["password"] == password:
                    return usuario["rol"]
            return None

    except FileNotFoundError:
        print("\nError: Archivo de administradores no encontrado.\n")
        return None
    except json.JSONDecodeError:
        print("\nError: Archivo JSON mal formado.\n")
        return None
    
def login_main():
    limpiar_pantalla()
    if login() == "s":
        nombre = input("ingresa tu nombre de usuario: ")
        contraseña = input("ingresa tu contraseña: ")
        rol = validarSesion(nombre, contraseña)

        if rol:
            limpiar_pantalla(2)
            if rol == "admin":
                print(f"bienvenido coordinador {nombre}")
                menuAdmin()
            elif rol == "camper":
                print(f"bienvenido camper {nombre}")
                menuCampers()
            elif rol == "trainer":
                print(f"bienvenido trainer {nombre}")
                menuTrainers()
            else:
                print("rol desconocido")
        else:
            print("acceso denegado")
    else:
        print("inicio de sesion cancelado")

if __name__ == "_main_":
    login_main()