import json
import os
from utils import limpiar_pantalla

ruta_usuarios = os.path.join(os.path.dirname(__file__), "usuarios.json")
ruta_notas = os.path.join(os.path.dirname(__file__), "notasCampers.json")
ruta_rutas = os.path.join(os.path.dirname(__file__), "rutas.json")
ruta_registro_trainer = os.path.join(os.path.dirname(__file__), "registroTrainers.json")

def cargar_registro_t():
    try:
        with open (ruta_registro_trainer, "r", encoding="utf-8") as archivoT:
            return json.load(archivoT)
    except FileNotFoundError:
        return []
        

def cargar_rutas():
    try: 
        with open (ruta_rutas, "r", encoding="utf-8") as archivoR :
            return json.load(archivoR)
    except FileNotFoundError:
        return []

def cargar_usuarios():
    try:
        with open(ruta_usuarios, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def cargar_notas():
    try:
        with open(ruta_notas, "r", encoding="utf-8") as archivoN:
            return json.load(archivoN)
    except FileNotFoundError:
        return {}

def listar_campers_inscritos():
    limpiar_pantalla()
    usuarios = cargar_usuarios()
    inscritos = [u for u in usuarios if u.get("rol") == "camper" and u.get("estado") == "inscrito"]

    print("\n--- Campers Inscritos ---")
    if inscritos:
        for c in inscritos:
            print(f"- {c['nombre']} {c['apellidos']}")
    else:
        print("No hay campers inscritos actualmente.")

def listar_campers_aprobados():
    limpiar_pantalla()
    usuarios = cargar_usuarios()
    aprobados = [u for u in usuarios if u.get("rol") == "camper" and u.get("estado") == "aprobado"]

    print("\n--- Campers que aprobaron el examen inicial ---")
    if aprobados:
        for c in aprobados:
            print(f"- {c['nombre']} {c['apellidos']}")
    else:
        print("No hay campers aprobados todavía.")

def listar_trainers_activos():
    limpiar_pantalla()
    usuarios = cargar_usuarios()  
    trainers = [u for u in usuarios if u.get("rol") == "trainer"]

    print("\n--- trainers activos ---")
    if trainers:
        for t in trainers:
            print(f"- {t['id']} {t['nombre']} {t['apellidos']} | Ruta: {t.get('ruta', 'Sin asignar')}")
    else:
        print("No hay trainers activos en este momento.")
    input("\n Presiona ENTER para continuar...")

def campers_bajo_rendimiento():
    limpiar_pantalla()
    notas = cargar_notas()

    print("\n--- Campers con bajo rendimiento (< 3.0) ---")
    encontrados = False
    for camper_id, datos in notas.items():
        modulos = datos.get("modulos", {})
        for modulo, lista_notas in modulos.items():
            if not lista_notas:
                continue
            promedio = sum(lista_notas) / len(lista_notas)
            if promedio < 3.0:
                print(f"{camper_id.replace('_',' ').title()} | Módulo: {modulo} | Promedio: {promedio:.2f}")
                encontrados = True
    if not encontrados:
        print("No hay campers con bajo rendimiento.")

def campers_y_trainers_por_ruta():
    limpiar_pantalla()
    usuarios = cargar_usuarios()
    rutas = {}

    for u in usuarios:
        ruta = u.get("ruta", "Sin asignar")
        if ruta not in rutas:
            rutas[ruta] = {"trainers": [], "campers": []}

        if u.get("rol") == "trainer":
            rutas[ruta]["trainers"].append(f"{u['nombre']} {u['apellidos']}")
        elif u.get("rol") == "camper":
            rutas[ruta]["campers"].append(f"{u['nombre']} {u['apellidos']}")

    print("\n--- Campers y Trainers por Ruta ---")
    for ruta, datos in rutas.items():
        print(f"\n📘 Ruta: {ruta}")
        print(" Trainers:", ", ".join(datos["trainers"]) if datos["trainers"] else "Ninguno")
        print(" Campers:", ", ".join(datos["campers"]) if datos["campers"] else "Ninguno")
    input("\nPresione ENTER para continuar...")

def resultados_por_modulo():
    limpiar_pantalla()
    notas = cargar_notas()
    resumen = {}

    print("\n--- Resultados por Módulo ---")
    for camper_id, datos in notas.items():
        ruta = datos.get("ruta", "Desconocida")
        trainer = datos.get("trainer", "Desconocido")
        for modulo, lista_notas in datos.get("modulos", {}).items():
            promedio = sum(lista_notas) / len(lista_notas)
            estado = "aprobado" if promedio >= 3.0 else "reprobado"

            resumen.setdefault(ruta, {}).setdefault(trainer, {}).setdefault(modulo, {"aprobados": 0, "reprobados": 0})
            resumen[ruta][trainer][modulo][f"{estado}s"] += 1

    for ruta, trainers in resumen.items():
        print(f"\n📘 Ruta: {ruta}")
        for trainer, modulos in trainers.items():
            print(f"  Trainer: {trainer}")
            for modulo, resultados in modulos.items():
                print(f"    - {modulo}: {resultados['aprobados']} aprobados | {resultados['reprobados']} reprobados")

def verReportes():
    print("\n--- Menú de Reportes ---")
    print("1. listar campers inscritos")
    print("2. listar campers que aprobaron el examen inicial")
    print("3. listar trainers activos(TEST)")
    print("4. campers con bajo rendimiento")
    print("5. campers y trainers por ruta")
    print("6. resultados por módulo")
    print("7. salir")
    return input("Seleccione una opción: ")

if __name__ == "__main__":
    while True:
        opcion = verReportes()
        limpiar_pantalla()
        if opcion == "1":
            listar_campers_inscritos()
        elif opcion == "2":
            listar_campers_aprobados()
        elif opcion == "3":
            listar_trainers_activos()
        elif opcion == "4":
            campers_bajo_rendimiento()
        elif opcion == "5":
            campers_y_trainers_por_ruta()
        elif opcion == "6":
            resultados_por_modulo()
        elif opcion == "7":
            print("Saliendo del menú de reportes...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        input("\nPresione ENTER para continuar...")