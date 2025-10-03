import json
import os

ruta_archivo_admin = os.path.join(os.path.dirname(__file__), "usuarios.json")

def login():

    print("""bienvenido a la base de datos de campus
        
    deseas iniciar sesion?(s/n)
        
    """)

    opcion = input().lower().strip()
    return opcion

def validarSesion(nombre, password):
    try:
        with open(ruta_archivo_admin, "r") as f:
            datos = json.load(f) 
        
        for admin in datos :
            if (

                admin ["nombre"] == nombre and
                admin ["password"] == password
            ):
                return admin["rol"]
        print("\nError: Credenciales incorrectas.\n")
        return None

    except FileNotFoundError:
        print("\nError: Archivo de administradores no encontrado.\n")
        return None
    except json.JSONDecodeError:
        print("\nError: Archivo JSON mal formado.\n")
        return None
    
def login_main():
    if login() == "s":
        nombre = input("ingresa tu nombre de usuario: ")
        contraseña = input("ingresa tu contraseña: ")
        rol = validarSesion(nombre, contraseña)

        if rol:
            if rol == "admin":
                print(f"bienvenido coordinador {nombre}")
            elif rol == "camper":
                print(f"bienvenido camper {nombre}")
            elif rol == "trainer":
                print(f"bienvenido trainer {nombre}")
            else:
                print("rol desconocido")
        else:
            print("acceso denegado")
    else:
        print("inicio de sesion cancelado")
