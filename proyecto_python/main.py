from login import login_main
from menuAdmin import *
from menuCampers import *
from menuTrainers import *     

ruta_archivo_admin = os.path.join(os.path.dirname(__file__), "usuarios.json")

def cargarUsuarios():
    try:
        with open(ruta_admin, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

if __name__ == "__main__":
    login_main()

if "rol" == "admin":
    menuAdmin()
elif "rol" == "camper":
    menuCampers()
elif "rol" == "trainer":
    menuTrainers()



