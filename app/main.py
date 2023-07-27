from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import credentials, auth, initialize_app
from google.cloud import firestore
from models import User, Course
from typing import List


app = FastAPI()

templates = Jinja2Templates(directory="src")
static_directory = "static"  # Ruta a la carpeta static de tu proyecto
static_files = StaticFiles(directory=static_directory)

app.mount("/static", static_files, name="static")

# Configuracion CORS
origins = ["*"]  # Agrega los orígenes permitidos aquí

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cred = credentials.Certificate("./certificate/lms-python-chile-firebase-adminsdk-wwtvi-9247aaf248.json")
firebase_admin.initialize_app(cred)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Ruta para el index
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



# Ruta para mostrar el formulario de inicio de sesión
@app.get("/login/", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Ruta para procesar el inicio de sesión
# Endpoint para procesar el inicio de sesión
@app.post("/login/")
async def login(request: Request):
    try:
        # Leer el token de acceso del encabezado de autorización
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Token de acceso no proporcionado")

        token = auth_header.split(" ")[1]

        # Verificar el token de acceso utilizando Firebase Authentication
        user_info = auth.verify_id_token(token)

        # Aquí puedes implementar la lógica para manejar los datos del usuario
        # Por ejemplo, puedes guardar los datos en una base de datos, crear una sesión, etc.
        # Luego, puedes devolver una respuesta adecuada para indicar que el inicio de sesión fue exitoso
        return {"message": "Inicio de sesión exitoso", "user_info": user_info}
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token de acceso expirado 1")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Token de acceso inválido 2")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al verificar el token de acceso 3")

# Endpoint protegido para acceder a los cursos (requiere autenticación)
@app.get("/cursos/", response_model=List[Course], dependencies=[Depends(oauth2_scheme)])
async def get_cursos():
    # Aquí puedes implementar la lógica para obtener los cursos de la base de datos y retornarlos como una lista de objetos Curso
    # Por ejemplo:
    # cursos = obtener_cursos_desde_la_base_de_datos()
    # return cursos
    return [{"nombre": "Curso de Python 1", "descripcion": "Introducción a Python"},
            {"nombre": "Curso de Python 2", "descripcion": "Avanzado de Python"}]




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)