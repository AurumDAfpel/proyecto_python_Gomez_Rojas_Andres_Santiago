import json
import os

ruta_registro = os.path.join(os.path.dirname(__file__), "usuarios.json")

def cargar_usuarios():
    try:
        with open(ruta_registro, "r") as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        usuarios = []
    return usuarios

def menuCampers():
    print("\n--- Menú Campers ---")
    print("1. ver notas")
    print("2. ver tareas")
    print("3. ver score")
    print("4. consultar riesgo")
    print("5. salir")
    return input("Seleccione una opción: ")

def verNotas(usuarios, usuario_actual):
    notas = usuario_actual.get("notas", [])
    if notas:
        print("\n--- Notas ---")
        for nota in notas:
            print(f"- {nota}")
    else:
        print("No hay notas registradas.")

def verTareas(usuarios, usuario_actual):
    tareas = usuario_actual.get("tareas", [])
    if tareas:
        print("\n--- Tareas ---")
        for tarea in tareas:
            print(f"- {tarea}")
    else:
        print("No hay tareas registradas.")

def verScore(usuarios, usuario_actual):
    score = usuario_actual.get("score", "No disponible")
    print(f"\n--- Score ---\nScore: {score}")

def consultarRiesgo(usuarios, usuario_actual):
    riesgo = usuario_actual.get("riesgo", "No disponible")
    print(f"\n--- Riesgo ---\nRiesgo: {riesgo}")

if __name__ == "__main__":
    usuarios = cargar_usuarios()
    usuario_actual = None

    print("Bienvenido al sistema de campers.")

    if usuarios:
        usuario_actual = usuarios[0]

    while True:
        opcion = menuCampers()

        if opcion == "1":
            verNotas(usuarios, usuario_actual)
        elif opcion == "2":
            verTareas(usuarios, usuario_actual)
        elif opcion == "3":
            verScore(usuarios, usuario_actual)
        elif opcion == "4":
            consultarRiesgo(usuarios, usuario_actual)