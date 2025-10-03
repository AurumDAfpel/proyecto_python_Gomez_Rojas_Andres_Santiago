import json
import os
ruta_admin = os.path.join(os.path.dirname(__file__), "usuarios.json")

def cargarUsuarios():
    try:
        with open(ruta_admin, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardarUsuarios(usuarios):
    with open(ruta_admin, "w") as f:
        json.dump(usuarios, f, indent=4)

def mostrarUsuarios():
    usuarios = cargarUsuarios()
    if not usuarios:
        print("no hay usuarios registrados")
        return
    print("\nusuarios resgistrados: ")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nombre']} - rol {usuario['rol']}") 

def registrarCamper():
    campers = cargarUsuarios()
    
    print("\n--- Registro de Nuevo Camper ---")
    camper = {
        "id": input("Número de identificación: ").strip(),
        "nombres": input("Nombres: ").strip(),
        "apellidos": input("Apellidos: ").strip(),
        "direccion": input("Dirección: ").strip(),
        "acudiente": input("Acudiente: ").strip(),
        "telefono_celular": input("Teléfono celular: ").strip(),
        "telefono_fijo": input("Teléfono fijo: ").strip(),
        "estado": "En proceso de ingreso",
        "riesgo": "N/A"
    }

    campers.append(camper)
    guardarUsuarios(campers)
    print(f"\nCamper {camper['nombres']} registrado con éxito.")

def actualizarEstadoCamper():
    campers = cargarUsuarios()
    mostrarUsuarios()
    if not campers:
        return
    try:
        seleccion = int(input("selecciona el numero del camper a actualizar: "))
        if 1<= seleccion <= len(campers):
            camper = campers[seleccion - 1]
            print(f"\nActualizando camper: {camper['nombres']} {camper['apellidos']}")
            nuevoEstado = input("ingresa el nuevo estado del camper (en proceso, inscrito, aprovadoCursando, Graduado, Expulsado, Retirado): ")
            nuevoRiesgo = input("ingresa el nuevo nivel de riesgo del camper(Bajo, Medio, Alto): ").strip()

            camper["estado"] = nuevoEstado
            camper["riesgo"] = nuevoRiesgo

            guardarUsuarios(campers)
            print("informacion actualizada correctamente")
        else:
            print("seleccion invalida")
    except ValueError:
        print("entrada invalida")

def menuAdmin():
    while True:
        print("""
--- GESTIÓN DE CAMPERS ---
1. Registrar nuevo camper
2. Ver campers
3. Actualizar estado/riesgo
4. Volver al menú anterior
""")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrarCamper()
        elif opcion == "2":
            mostrarUsuarios()
        elif opcion == "3":
            actualizarEstadoCamper()
        elif opcion == "4":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menuAdmin()
    

