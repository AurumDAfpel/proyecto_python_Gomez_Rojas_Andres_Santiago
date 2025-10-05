import json
import os
from utils import limpiar_pantalla
from reportes import verReportes

ruta_admin = os.path.join(os.path.dirname(__file__), "usuarios.json")
ruta_cursos = os.path.join(os.path.dirname(__file__), "rutas.json")
ruta_reportes = os.path.join(os.path.dirname(__file__), "reportes.json")
ruta_credenciales = os.path.join(os.path.dirname(__file__), "credenciales.json")

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
    if not usuarios:
        print("no hay usuarios registrados")
        return
    print("\nusuarios resgistrados: ")
    for i, usuario in enumerate(usuarios, 1):
        nombre = usuario.get('nombre') or f"{usuario.get('nombres', '')} {usuario.get('apellidos', '')}".strip()
        rol = usuario.get('rol') 
        
        print(f"{i}. {nombre} - rol {rol}")

def registrarUsiarios():
    campers = cargarUsuarios()
    
    print("\n--- Registro de Nuevo Camper ---")
    camper = {
        "id": input("Número de identificación: ").strip(),
        "nombre": input("Nombres: ").strip(),
        "apellidos": input("Apellidos: ").strip(),
        "direccion": input("Dirección: ").strip(),
        "acudiente": input("Acudiente: ").strip(),
        "telefono_celular": input("Teléfono celular: ").strip(),
        "telefono_fijo": input("Teléfono fijo: ").strip(),
        "estado": "En proceso de ingreso",
        "riesgo": "N/A",
        "rol": "camper"
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

def registrarTrainer():
    trainers = cargarUsuarios()
    
    print("\n--- Registro de Nuevo Trainer ---")
    trainer = {
        "id": input("Número de identificación: ").strip(),
        "nombre": input("Nombres: ").strip(),
        "apellidos": input("Apellidos: ").strip(),
        "especialidad": input("Especialidad: ").strip(),
        "telefono_celular": input("Teléfono celular: ").strip(),
        "telefono_fijo": input("Teléfono fijo: ").strip(),
        "rol": "trainer"
    }

    trainers.append(trainer)
    guardarUsuarios(trainers)
    print(f"\nTrainer {trainer['nombres']} registrado con éxito.")

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
        print(f"{i}. {trainer['nombres']} {trainer['apellidos']} - especialidad: {trainer['especialidad']}")

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
    campers = [u for u in usuarios if u.get("rol") == "camper"]
    if not campers:
        print("no hay campers registrados")
        return
    print("\n--- Notas de Campers ---")
    for camper in campers:
        notas = camper.get("notas", [])
        print(f"{camper['nombre']} {camper['apellidos']}: {', '.join(notas) if notas else 'No hay notas registradas.'}")

def crearHorario(): 
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
                    print(f" ERROR: La actividad '{actividad}' ya ha sido registrada en otro día/franja. Intente con otra.")
                    continue
                else:
                    actividades_registradas.add(actividad_limpia)
                    horario_dia[franja] = actividad
                    break
        
        horario[dia] = horario_dia

    with open(ruta_reportes, "w") as f:
        json.dump(horario, f, indent=4)
    
    print("\n Horario creado con éxito.")

def verHorario():
    try:
        with open(ruta_reportes, "r") as f:
            horario = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hay un horario creado aún.")
        return
    
    print("\n--- Horario Semanal ---")
    for dia, franjas in horario.items():
        print(f"\n{dia}:")
        for franja, actividad in franjas.items():
            print(f"  {franja}: {actividad}")

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
7. agregar rutas
8. ver reportes
9. ver trainers
10. Registrar nuevas credenciales
11. ver notas de los campers
12. crear horario
13. ver horario
14. salir
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
            agregarRutas()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "8":
            verReportes()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "9":
            mostrarTrainers()  
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "10":
            registrarCredenciales()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "11": 
            verNotasCampers()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "12":
            crearHorario()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "13":
            verHorario()
            input("Presiona ENTER para continuar...")
            limpiar_pantalla()
        elif opcion == "14":
            break
        else:
            print("Opción inválida.")
