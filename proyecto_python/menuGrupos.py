import json
from utils import limpiar_pantalla
import os

ruta_Grupos = os.path.join(os.path.dirname(__file__), "grupos.json")
ruta_registro = os.path.join(os.path.dirname(__file__), "usuarios.json")


def cargar_grupos():
    try:
        with open(ruta_Grupos, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
            return data.get("grupos", [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error al leer el archivo de grupos. Asegúrese de que el formato sea correcto.")
        return []
    
def guardar_grupos(grupos):
    with open(ruta_Grupos, "w", encoding="utf-8") as archivo:
        json.dump({"grupos": grupos}, archivo, indent=4)

def cargarUsuarios():
    try:
        with open(ruta_registro, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def crearGrupo():
    limpiar_pantalla()
    grupos = cargar_grupos()
    nombre_grupo = input("Ingrese el nombre del nuevo grupo: ").strip()

    if any(g['nombre'] == nombre_grupo for g in grupos):
        print("Ya existe un grupo con ese nombre.")
        return

    nuevo_grupo = {
        "nombre": nombre_grupo,
        "campers": [],
        "trainers": []
    }
    grupos.append(nuevo_grupo)
    guardar_grupos(grupos)
    print(f"Grupo '{nombre_grupo}' creado exitosamente.")

def verGrupos():
    limpiar_pantalla()
    grupos = cargar_grupos()

    if not grupos:
        print("No hay grupos creados.")
        return

    print("\n--- Grupos Existentes ---")
    for grupo in grupos:
        print(f"Grupo: {grupo['nombre']} | Campers: {', '.join(grupo['campers']) if grupo['campers'] else 'Ninguno'}")

def asignarCampersAGrupo():
    limpiar_pantalla()
    grupos = cargar_grupos()
    usuarios = cargarUsuarios()
    campers = [u for u in usuarios if u.get("rol") == "camper"]

    if not grupos:
        print("No hay grupos creados. Cree un grupo primero.")
        return

    if not campers:
        print("No hay campers registrados.")
        return

    print("\n--- Grupos Disponibles ---")
    for idx, grupo in enumerate(grupos, start=1):
        print(f"{idx}. {grupo['nombre']}")

    try:
        seleccion_grupo = int(input("Seleccione el número del grupo al que desea asignar campers: ")) - 1
        if seleccion_grupo < 0 or seleccion_grupo >= len(grupos):
            print("Selección inválida.")
            return
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")
        return

    grupo_seleccionado = grupos[seleccion_grupo]

    print("\n--- Campers Disponibles ---")
    for idx, camper in enumerate(campers, start=1):
        print(f"{idx}. {camper['nombre']} {camper['apellidos']}")

    seleccion_campers = input("Ingrese los números de los campers a asignar (separados por comas): ")
    try:
        indices_campers = [int(i.strip()) - 1 for i in seleccion_campers.split(",")]
        for idx in indices_campers:
            if 0 <= idx < len(campers):
                camper_nombre = f"{campers[idx]['nombre']} {campers[idx]['apellidos']}"
                if camper_nombre not in grupo_seleccionado['campers']:
                    grupo_seleccionado['campers'].append(camper_nombre)
            else:
                print(f"Número de camper inválido: {idx + 1}")
    except ValueError:
        print("Entrada inválida. Asegúrese de ingresar números separados por comas.")
        return

    guardar_grupos(grupos)
    print(f"Campers asignados al grupo '{grupo_seleccionado['nombre']}' exitosamente.")

def asignarHorarioAGrupo():
    limpiar_pantalla()
    grupos = cargar_grupos()
    if not grupos:
        print("No hay grupos creados. Cree un grupo primero.")
        return
    print("\n--- Grupos Disponibles ---")
    for idx, grupo in enumerate(grupos, start=1):
        print(f"{idx}. {grupo['nombre']}")
    try:
        seleccion_grupo = int(input("Seleccione el número del grupo al que desea asignar un horario: ")) - 1
        if seleccion_grupo < 0 or seleccion_grupo >= len(grupos):
            print("Selección inválida.")
            return
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")
        return
    grupo_seleccionado = grupos[seleccion_grupo]
    print(f"\nAsignando horario al grupo: {grupo_seleccionado['nombre']}")
    print("\n--- Crear Horario ---")
    franjas_horarias = [
        "06:00 - 10:00", 
        "10:00 - 14:00", 
        "14:00 - 18:00", 
        "18:00 - 22:00"
    ]
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    horario = {}
    actividades_registradas = set()
    for dia in dias:
        print(f"\n--- {dia} ---")
        horario_dia = {}
        for franja in franjas_horarias:
            while True:
                actividad = input(f"[{franja}] Ingrese la actividad (o deje vacío si no hay): ").strip()
                if not actividad:
                    horario_dia[franja] = "Descanso/Libre"
                    break
                actividad_limpia = actividad.lower()
                if actividad_limpia in actividades_registradas:
                    print(f"❌ La actividad '{actividad}' ya ha sido registrada en otro día/franja horaria. Intente otra.")
                    continue
                else:
                    actividades_registradas.add(actividad_limpia)
                    horario_dia[franja] = actividad
                    break
        horario[dia] = horario_dia
    grupo_seleccionado["horario"] = horario
    guardar_grupos(grupos)
    print("\nHorario asignado con éxito al grupo.")

def verHorarioDeGrupo():    
    limpiar_pantalla()
    grupos = cargar_grupos()
    if not grupos:
        print("No hay grupos creados.")
        return
    print("\n--- Grupos Disponibles ---")
    for idx, grupo in enumerate(grupos, start=1):
        print(f"{idx}. {grupo['nombre']}")
    try:
        seleccion_grupo = int(input("Seleccione el número del grupo cuyo horario desea ver: ")) - 1
        if seleccion_grupo < 0 or seleccion_grupo >= len(grupos):
            print("Selección inválida.")
            return
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")
        return
    grupo_seleccionado = grupos[seleccion_grupo]
    horario = grupo_seleccionado.get("horario")
    if not horario:
        print(f"El grupo '{grupo_seleccionado['nombre']}' no tiene un horario asignado.")
        return
    print(f"\n--- Horario del Grupo: {grupo_seleccionado['nombre']} ---")
    for dia, franjas in horario.items():
        print(f"\n{dia}:")
        for franja, actividad in franjas.items():
            print(f"  {franja}: {actividad}")
def eliminarGrupo():
    limpiar_pantalla()
    grupos = cargar_grupos()
    if not grupos:
        print("No hay grupos creados.")
        return
    print("\n--- Grupos Disponibles ---")
    for idx, grupo in enumerate(grupos, start=1):
        print(f"{idx}. {grupo['nombre']}")
    try:
        seleccion_grupo = int(input("Seleccione el número del grupo que desea eliminar: ")) - 1
        if seleccion_grupo < 0 or seleccion_grupo >= len(grupos):
            print("Selección inválida.")
            return
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")
        return
    grupo_eliminado = grupos.pop(seleccion_grupo)
    guardar_grupos(grupos)
    print(f"Grupo '{grupo_eliminado['nombre']}' eliminado exitosamente.")

def asignarTrainersAGrupos():
    limpiar_pantalla()
    grupos = cargar_grupos()
    usuarios = cargarUsuarios()
    trainers = [u for u in usuarios if u.get("rol") == "trainer"]

    if not grupos:
        print("No hay grupos creados. Cree un grupo primero.")
        return

    if not trainers:
        print("No hay trainers registrados.")
        return

    print("\n--- Grupos Disponibles ---")
    for idx, grupo in enumerate(grupos, start=1):
        print(f"{idx}. {grupo['nombre']}")

    try:
        seleccion_grupo = int(input("Seleccione el número del grupo al que desea asignar trainers: ")) - 1
        if seleccion_grupo < 0 or seleccion_grupo >= len(grupos):
            print("Selección inválida.")
            return
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número.")
        return

    grupo_seleccionado = grupos[seleccion_grupo]

    print("\n--- trainers Disponibles ---")
    for idx, trainer in enumerate(trainers, start=1):
        print(f"{idx}. {trainer['nombre']} {trainer['apellidos']}")

    seleccion_trainer = input("Ingrese los números de los trainers a asignar (separados por comas): ")
    try:
        indices_trainers = [int(i.strip()) - 1 for i in seleccion_trainer.split(",")]
        for idx in indices_trainers:
            if 0 <= idx < len(trainers):
                trainer_nombre = f"{trainer[idx]['nombre']} {trainer[idx]['apellidos']}"
                if trainer_nombre not in grupo_seleccionado['trainers']:
                    grupo_seleccionado['trainers'].append(trainer_nombre)
            else:
                print(f"Número de trainer inválido: {idx + 1}")
    except ValueError:
        print("Entrada inválida. Asegúrese de ingresar números separados por comas.")
        return

    guardar_grupos(grupos)
    print(f"trainers asignados al grupo '{grupo_seleccionado['nombre']}' exitosamente.")


def menuGrupos():
    while True:
        print("""
--- Menú de Grupos ---
1. crear grupo
2. ver grupos
3. asignar campers a grupo
4. asignar trainers a grupo
5. asignar horario a grupo
6. ver horario de grupo
7. eliminar grupo
8. salir
""")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            crearGrupo()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "2":
            verGrupos()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "3":
            asignarCampersAGrupo()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion =="4":
            asignarTrainersAGrupos()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "5":
            asignarHorarioAGrupo()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "6":
            verHorarioDeGrupo()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "7":
            eliminarGrupo()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "8":
            break
        else:
            print("Opción inválida.")