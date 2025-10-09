import json
import os
from utils import limpiar_pantalla
from reportes import verReportes
from menuGrupos import menuGrupos

ruta_admin = os.path.join(os.path.dirname(__file__), "usuarios.json")
ruta_cursos = os.path.join(os.path.dirname(__file__), "rutas.json")
ruta_reportes = os.path.join(os.path.dirname(__file__), "reportes.json")
ruta_credenciales = os.path.join(os.path.dirname(__file__), "credenciales.json")
ruta_notas = os.path.join(os.path.dirname(__file__), "notasCampers.json")  
ruta_registro_t = os.path.join(os.path.dirname(__file__), "registroTrainers.json")

def cargar_registro_t():
    try:
        with open (ruta_registro_t, "r", encoding="utf-8") as archivoT:
            return json.load(archivoT)
    except FileNotFoundError:
        return []
        

def cargarUsuarios():
    try:
        with open(ruta_admin, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def cargarRutas():
    try:
        with open(ruta_cursos, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardarUsuarios(usuarios):
    with open(ruta_admin, "w") as f:
        json.dump(usuarios, f, indent=4)

def mostrarUsuarios():
    usuarios = cargarUsuarios()
    campers = [u for u in usuarios if u.get("rol") == "camper"]

    if not campers:
        print("No hay campers registrados.")
        return

    print("\n--- Campers Registrados ---")
    for i, usuario in enumerate(campers, 1):
        nombre = usuario.get('nombre', '').strip()
        apellidos = usuario.get('apellidos', '').strip()
        nombre_completo = f"{nombre} {apellidos}".strip()
        print(f"{i}. {nombre_completo}")

def registrarUsiarios():
    campers = cargarUsuarios()
    
    print("\n--- Registro de Nuevo Camper ---")
    camper = {
        "id": input("Número de identificación: ").strip(),
        "nombre": input("Nombre: ").strip(),
        "apellidos": input("Apellidos: ").strip(),
        "direccion": input("Dirección: ").strip(),
        "acudiente": input("Acudiente: ").strip(),
        "telefono_celular": input("Teléfono celular: ").strip(),
        "telefono_fijo": input("Teléfono fijo: ").strip(),
        "estado": "En proceso de ingreso",
        "riesgo": "N/A",
        "rol": "camper",
        "ruta": "N/A"
    }

    campers.append(camper)
    guardarUsuarios(campers)
    print(f"\nCamper {camper['nombre']} registrado con éxito.")

def actualizarEstadoCamper():
    campers = cargarUsuarios()
    mostrarUsuarios()
    if not campers:
        return
    try:
        seleccion = int(input("selecciona el numero del camper a actualizar: "))
        if 1<= seleccion <= len(campers):
            camper = campers[seleccion - 1]
            print(f"\nActualizando camper: {camper['nombre']} {camper['apellidos']}")
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

def registrarTrainer():
    trainers = cargar_registro_t()
    
    print("\n--- Registro de Nuevo Trainer ---")
    trainer = {
        "id": input("Número de identificación: ").strip(),
        "nombre": input("Nombre: ").strip(),
        "apellidos": input("Apellidos: ").strip(),
        "especialidad": input("Especialidad(lenguaje de programacion): ").strip(),
        "telefono_celular": input("Teléfono celular: ").strip(),
        "telefono_fijo": input("Teléfono fijo: ").strip(),
        "rol": "trainer",
        "ruta": "N/A"
    }

    trainers.append(trainer)
    guardarUsuarios(trainers)
    print(f"\nTrainer {trainer['nombre']} registrado con éxito.")

def rutasDisponibles():
    rutas = cargarRutas()
    if not rutas:
        print("no hay rutas disponibles")
        return
    print("\nrutas disponibles: ")
    for i, ruta in enumerate(rutas, 1):
        print(f"{i}. {ruta['ruta']} - descripcion: {ruta['descripcion']}")

def contarCampersPorRuta(usuarios, nombre_ruta):

    contador = 0
    for camper in usuarios:
        rutas_asignadas = camper.get("rutas", [])
        for ruta_dict in rutas_asignadas:
            if ruta_dict.get("nombre") == nombre_ruta:
                contador += 1
                break
    return contador

def agregarRutaCamper():
    todos_usuarios = cargarUsuarios() 
    rutas = cargarRutas()
    
    campers_filtrados = [u for u in todos_usuarios if u.get('rol', '').lower() == 'camper']
    
    if not campers_filtrados:
        print("No hay campers disponibles para asignar rutas.")
        return

    print("\n--- Campers Disponibles para Asignar Ruta ---")
    for i, camper in enumerate(campers_filtrados, 1):
        nombre = camper.get('nombre', '')
        apellidos = camper.get('apellidos', '')
        print(f"{i}. {nombre} {apellidos}")
        
    try:
        seleccion = int(input("selecciona el numero del camper para asignar ruta: "))
        
        if 1 <= seleccion <= len(campers_filtrados):
            camper = campers_filtrados[seleccion - 1]
            
            nombre_camper = camper.get('nombre', '')
            apellidos_camper = camper.get('apellidos', '')
            print(f"\nAsignando ruta a camper: {nombre_camper} {apellidos_camper}")
            
            rutasDisponibles() 
            if not rutas:
                return
            
            rutaSeleccionada = int(input("selecciona el numero de la ruta a asignar: "))
            
            if 1 <= rutaSeleccionada <= len(rutas):
                ruta = rutas[rutaSeleccionada - 1]
                nombre_ruta = ruta['ruta']

                guardarUsuarios(todos_usuarios)
                
            else:
                print("seleccion de ruta invalida")
        else:
            print("seleccion de camper invalida")
    except ValueError:
        print("entrada invalida")

def agregarRutas():
    rutas = cargarRutas()
    
    print("\n--- Agregar Nueva Ruta ---")
    ruta = {
        "id": input("ID de la ruta: ").strip(),
        "ruta": input("Nombre de la ruta: ").strip(),
        "descripcion": input("Descripción de la ruta: ").strip()
    }

    rutas.append(ruta)
    with open(ruta_cursos, "w") as f:
        json.dump(rutas, f, indent=4)
    print(f"\nRuta {ruta['ruta']} agregada con éxito.")

def mostrarTrainers():
    usuarios = cargarUsuarios()
    trainers = [u for u in usuarios if u.get("rol") == "trainer"]
    if not trainers:
        print("no hay trainers registrados")
        return
    print("\ntrainers resgistrados: ")
    for i, trainer in enumerate(trainers, 1):
        print(f"{i}. {trainer['nombre']} {trainer['apellidos']} - especialidad: {trainer['especialidad']}")

def cargarCredenciales():
    try:
        with open(ruta_credenciales, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def guardarCredenciales(credenciales):
    with open(ruta_credenciales, "w") as f:
        json.dump(credenciales, f, indent=4)

def registrarCredenciales():
    credenciales = cargarCredenciales()
    
    print("\n--- Registro de Nuevas Credenciales ---")
    nueva_credencial = {
        "nombre": input("Nombre de usuario: ").strip(),
        "password": input("Contraseña: ").strip(),
        "estado": "activo",
        "riesgo": "N/A",
        "rol": input("Rol (admin/camper/trainer): ").strip()
    }

    credenciales.append(nueva_credencial)
    guardarCredenciales(credenciales)
    print(f"\nCredenciales para {nueva_credencial['nombre']} registradas con éxito.")

def verNotasCampers():
    usuarios = cargarUsuarios()
    notas = cargar_notas()
    campers = [u for u in usuarios if u.get("rol") == "camper"]
    if not campers:
        print("no hay campers registrados")
        return
    print("\n--- Notas de Campers ---")
    for i, camper in enumerate(campers, 1):
        camper_id = f"{camper['nombre']}_{camper['apellidos']}".replace(" ", "_").lower()
        notas_camper = notas.get(camper_id, [])
        print(f"{i}. {camper['nombre']} {camper['apellidos']} - Notas: {notas_camper if notas_camper else 'No hay notas registradas.'}")

def cargar_notas():
    try:
        with open(ruta_notas, "r") as archivo:
            notas = json.load(archivo)
    except FileNotFoundError:
        notas = {}
    return notas

def administrarNotas(usuarios): 
    limpiar_pantalla()
    usuarios = cargarUsuarios()
    notas = cargar_notas()
    print("\n--- Administrar Notas ---")
    for i, usuario in enumerate(usuarios, 1):
        print(f"{i}. {usuario['nombre']} {usuario['apellidos']}")
    seleccion = int(input("Seleccione el número del camper para administrar notas: ")) - 1
    if 0 <= seleccion < len(usuarios):
        camper = usuarios[seleccion]
        camper_id = f"{camper['nombre']}_{camper['apellidos']}".replace(" ", "_").lower()
        print(f"\nCamper seleccionado: {camper['nombre']} {camper['apellidos']}")
        print("Notas actuales:", notas.get(camper_id, []))
        nueva_nota = input("Ingrese la nueva nota (o 'salir' para regresar): ")
        if nueva_nota.lower() != 'salir':
            if camper_id not in notas:
                notas[camper_id] = []
            notas[camper_id].append(nueva_nota)
            with open(ruta_notas, "w", encoding="utf-8") as archivo:
                json.dump(notas, archivo, indent=4)
            print("Nota agregada con éxito.")
    else:
        print("Selección inválida.")

def eliminarCamper():
    usuarios = cargarUsuarios()
    mostrarUsuarios()
    if not usuarios:
        return
    try:
        seleccion = int(input("selecciona el numero del camper a eliminar: "))
        if 1<= seleccion <= len(usuarios):
            usuario = usuarios[seleccion - 1]
            if usuario.get("rol") != "camper":
                print("El usuario seleccionado no es un camper.")
                return
            confirmacion = input(f"¿Está seguro de que desea eliminar al camper {usuario['nombre']} {usuario['apellidos']}? (s/n): ").strip().lower()
            if confirmacion == 's':
                usuarios.remove(usuario)
                guardarUsuarios(usuarios)
                print("Camper eliminado correctamente.")
            else:
                print("Eliminación cancelada.")
        else:
            print("seleccion invalida")
    except ValueError:
        print("entrada invalida")

def eliminarTrainer():
    usuarios = cargarUsuarios()
    mostrarUsuarios()
    if not usuarios:
        return
    try:
        seleccion = int(input("selecciona el numero del trainer a eliminar: "))
        if 1<= seleccion <= len(usuarios):
            usuario = usuarios[seleccion - 1]
            if usuario.get("rol") != "trainer":
                print("El usuario seleccionado no es un trainer.")
                return
            confirmacion = input(f"¿Está seguro de que desea eliminar al trainer {usuario['nombre']} {usuario['apellidos']}? (s/n): ").strip().lower()
            if confirmacion == 's':
                usuarios.remove(usuario)
                guardarUsuarios(usuarios)
                print("Trainer eliminado correctamente.")
            else:
                print("Eliminación cancelada.")
        else:
            print("seleccion invalida")
    except ValueError:
        print("entrada invalida")   

def agregarRutaTrainer():
    todos_usuarios = cargarUsuarios() 
    rutas = cargarRutas()
    
    trainer_filtrados = [u for u in todos_usuarios if u.get('rol', '').lower() == 'trainer']
    
    if not trainer_filtrados:
        print("No hay campers disponibles para asignar rutas.")
        return

    print("\n--- trainers Disponibles para Asignar Ruta ---")
    for i, trainer in enumerate(trainer_filtrados, 1):
        nombre = trainer.get('nombre', '')
        apellidos = trainer.get('apellidos', '')
        print(f"{i}. {nombre} {apellidos}")
        
    try:
        seleccion = int(input("selecciona el numero del trainer para asignar ruta: "))
        
        if 1 <= seleccion <= len(trainer_filtrados):
            camper = trainer_filtrados[seleccion - 1]
            
            nombre_trainer = trainer.get('nombre', '')
            apellidos_trainer = trainer.get('apellidos', '')
            print(f"\nAsignando ruta a camper: {nombre_trainer} {apellidos_trainer}")
            
            rutasDisponibles() 
            if not rutas:
                return
            
            rutaSeleccionada = int(input("selecciona el numero de la ruta a asignar: "))
            
            if 1 <= rutaSeleccionada <= len(rutas):
                ruta = rutas[rutaSeleccionada - 1]
                nombre_ruta = ruta['ruta']

                guardarUsuarios(todos_usuarios)
                
            else:
                print("seleccion de ruta invalida")
        else:
            print("seleccion de camper invalida")
    except ValueError:
        print("entrada invalida")

def menuAdmin():
    while True:
        print("""
--- GESTIÓN DE campus ---
1. Registrar nuevo camper
2. Ver campers
3. Actualizar estado/riesgo
4. Registrar nuevo trainer
5. revisar rutas disponibles
6. Agregar ruta a camper
7. agregar ruta a trainer              
8. agregar rutas
9. ver reportes
10. ver trainers
11. Registrar nuevas credenciales
12. ver notas de los campers
13. asignar notas a campers
14. grupos
15. eliminar campers
16. eliminar trainers
17. salir
""")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrarUsiarios()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "2":
            mostrarUsuarios()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "3":
            actualizarEstadoCamper()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "4":
            registrarTrainer()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "5":
            rutasDisponibles()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "6":
            agregarRutaCamper()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "7":
            agregarRutaTrainer()
            input("Presione ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "8":
            agregarRutas()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "9":
            verReportes()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "10":
            mostrarTrainers()  
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "11":
            registrarCredenciales()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "12": 
            verNotasCampers()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "13":
            administrarNotas(cargarUsuarios())
            limpiar_pantalla()
            input("Presiona ENTER para continuar...")
        elif opcion == "14":
            menuGrupos()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "15":
            eliminarCamper()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "16":
            eliminarTrainer()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "17":
            break
        else:
            print("Opción inválida.")