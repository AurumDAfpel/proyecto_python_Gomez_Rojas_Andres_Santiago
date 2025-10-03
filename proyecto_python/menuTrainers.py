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

def menuTrainers():
    print("\n--- Menú Trainers ---")
    print("1. administrar notas")
    print("2. asignar tareas")
    print("3. ruta y campers asignados")
    print("4. administrar evaluaciones")
    print("5. salir")
    return input("Seleccione una opción: ")

def administrarNotas(usuarios):
    print("\n--- Administrar Notas ---")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nombres']} {usuario['apellidos']}")
    seleccion = int(input("Seleccione el número del camper para administrar notas: ")) - 1
    if 0 <= seleccion < len(usuarios):
        camper = usuarios[seleccion]
        print(f"\nCamper seleccionado: {camper['nombres']} {camper['apellidos']}")
        print("Notas actuales:", camper.get("notas", []))
        nueva_nota = input("Ingrese la nueva nota (o 'salir' para regresar): ")
        if nueva_nota.lower() != 'salir':
            if "notas" not in camper:
                camper["notas"] = []
            camper["notas"].append(nueva_nota)
            with open(ruta_registro, "w") as archivo:
                json.dump(usuarios, archivo, indent=4)
            print("Nota agregada con éxito.")
    else:
        print("Selección inválida.")

def asignarTareas(usuarios):
    print("\n--- Asignar Tareas ---")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nombres']} {usuario['apellidos']}")
    seleccion = int(input("Seleccione el número del camper para asignar tareas: ")) - 1
    if 0 <= seleccion < len(usuarios):
        camper = usuarios[seleccion]
        print(f"\nCamper seleccionado: {camper['nombres']} {camper['apellidos']}")
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
        rutas[ruta].append(f"{usuario['nombres']} {usuario['apellidos']}")
    for ruta, campers in rutas.items():
        print(f"\nRuta: {ruta}")
        for camper in campers:
            print(f"- {camper}")

def administrarEvaluaciones(usuarios):
    print("\n--- Administrar Evaluaciones ---")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nombres']} {usuario['apellidos']}")
    seleccion = int(input("Seleccione el número del camper para administrar evaluaciones: ")) - 1
    if 0 <= seleccion < len(usuarios):
        camper = usuarios[seleccion]
        print(f"\nCamper seleccionado: {camper['nombres']} {camper['apellidos']}")
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

if __name__ == "__main__":
    usuarios = cargar_usuarios()
    while True:
        opcion = menuTrainers()
        if opcion == "1":
            administrarNotas(usuarios)
        elif opcion == "2":
            asignarTareas(usuarios)
        elif opcion == "3":
            rutaYCampersAsignados(usuarios)
        elif opcion =="4":
            administrarEvaluaciones(usuarios)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")
