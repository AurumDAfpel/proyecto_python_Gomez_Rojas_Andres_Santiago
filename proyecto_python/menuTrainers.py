import json
import os
from utils import limpiar_pantalla

ruta_registro = os.path.join(os.path.dirname(__file__), "usuarios.json")
ruta_notas = os.path.join(os.path.dirname(__file__), "notasCampers.json")

def cargar_usuarios():
    try:
        with open(ruta_registro, "r") as archivo:
            usuarios = json.load(archivo)
    except FileNotFoundError:
        usuarios = []
    return usuarios

def cargar_notas():
    try:
        with open(ruta_notas, "r") as archivo:
            notas = json.load(archivo)
    except FileNotFoundError:
        notas = {}
    return notas

def menuTrainers():
    print("\n--- Menú Trainers ---")
    print("1. asignar tareas")
    print("2. ruta y campers asignados")
    print("3. administrar evaluaciones")
    print("4. revisar promedio")
    print("5. salir")
    return input("Seleccione una opción: ")

def verPromedios():
    limpiar_pantalla()
    notas = cargar_notas()

    if not notas:
        print("\n No hay notas registradas todavía.")
        return
    

    print("\n--- Promedios de Campers ---")
    for camper_id, lista_notas in notas.items():
        try:

            notas_flotantes = [float(n) for n in lista_notas]
        except ValueError:
            print(f" Error: Hay notas no numéricas en {camper_id}.")
            continue

        promedio = sum(notas_flotantes) / len(notas_flotantes)
        estado = " Aprobado" if promedio >= 60 else " Reprobado"

        nombre = camper_id.replace("_", " ").title()
        print(f"\n {nombre}")
        print(f"Notas: {notas_flotantes}")
        print(f"Promedio: {promedio:.2f} | Estado: {estado}")

def asignarTareas(usuarios):
    print("\n--- Asignar Tareas ---")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nombre']} {usuario['apellidos']}")
    seleccion = int(input("Seleccione el número del camper para asignar tareas: ")) - 1
    if 0 <= seleccion < len(usuarios):
        camper = usuarios[seleccion]
        print(f"\nCamper seleccionado: {camper['nombre']} {camper['apellidos']}")
        print("Tareas actuales:", camper.get("tareas", []))
        nueva_tarea = input("Ingrese la nueva tarea (o 'salir' para regresar): ")
        if nueva_tarea.lower() != 'salir':
            if "tareas" not in camper:
                camper["tareas"] = []
            camper["tareas"].append(nueva_tarea)
            with open(ruta_registro, "w") as archivo:
                json.dump(usuarios, archivo, indent=4)
            print("Tarea asignada con éxito.")
    else:
        print("Selección inválida.")

def rutaYCampersAsignados(usuarios):
    print("\n--- Ruta y Campers Asignados ---")
    rutas = {}
    for usuario in usuarios:
        ruta = usuario.get("ruta", "No asignada")
        if ruta not in rutas:
            rutas[ruta] = []
        rutas[ruta].append(f"{usuario['nombre']} {usuario['apellidos']}")
    for ruta, campers in rutas.items():
        print(f"\nRuta: {ruta}")
        for camper in campers:
            print(f"- {camper}")

def administrarEvaluaciones(usuarios):
    print("\n--- Administrar Evaluaciones ---")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nombre']} {usuario['apellidos']}")
    seleccion = int(input("Seleccione el número del camper para administrar evaluaciones: ")) - 1
    if 0 <= seleccion < len(usuarios):
        camper = usuarios[seleccion]
        print(f"\nCamper seleccionado: {camper['nombre']} {camper['apellidos']}")
        print("Evaluaciones actuales:", camper.get("evaluaciones", []))
        nueva_evaluacion = input("Ingrese la nueva evaluación (o 'salir' para regresar): ")
        if nueva_evaluacion.lower() != 'salir':
            if "evaluaciones" not in camper:
                camper["evaluaciones"] = []
            camper["evaluaciones"].append(nueva_evaluacion)
            with open(ruta_registro, "w") as archivo:
                json.dump(usuarios, archivo, indent=4)
            print("Evaluación agregada con éxito.")
    else:
        print("Selección inválida.")
    
def verRutas():
    print("\n--- Ver Rutas Disponibles ---")
    rutas_disponibles = set()
    usuarios = cargar_usuarios()
    for usuario in usuarios:
        ruta = usuario.get("ruta")
        if ruta:
            rutas_disponibles.add(ruta)
    if rutas_disponibles:
        print("Rutas disponibles:")
        for ruta in rutas_disponibles:
            print(f"- {ruta}")
    else:
        print("No hay rutas asignadas.")

if __name__ == "__main__":
    usuarios = cargar_usuarios()
    while True:
        limpiar_pantalla(2)
        opcion = menuTrainers()
        if opcion == "1":
            asignarTareas(usuarios)
            limpiar_pantalla()
            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            rutaYCampersAsignados(usuarios)
            limpiar_pantalla()
            input("Presiona ENTER para continuar...")
        elif opcion =="3":
            administrarEvaluaciones(usuarios)
            limpiar_pantalla()
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            verPromedios()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")
