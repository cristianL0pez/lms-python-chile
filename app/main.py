from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import credentials
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


# Función para verificar el token de acceso
def verify_token(token: str = Depends(oauth2_scheme)):
    # Aquí puedes implementar la lógica para verificar y decodificar el token de acceso
    # Si el token es válido, puedes obtener los datos del usuario y devolverlos en un modelo
    # Si el token es inválido, puedes lanzar una excepción HTTP con el mensaje "Token de acceso inválido"

    # Ejemplo:
    # user_data = decode_jwt_token(token)
    # return user_data

    # Si aún no tienes implementada la lógica de verificación del token, puedes simplemente devolver el token por ahora:
    return token

# Endpoint para procesar el inicio de sesión
@app.post("/login/")
async def login(user_data: dict, token: str = Depends(verify_token)):
    try:
        # Aquí puedes implementar la lógica para manejar los datos del usuario
        # Por ejemplo, puedes guardar los datos en una base de datos, crear una sesión, etc.
        # Luego, puedes devolver una respuesta adecuada para indicar que el inicio de sesión fue exitos
        
        return {"message": "Inicio de sesión exitoso", "user_data": user_data }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al procesar el inicio de sesión")


# Endpoint protegido para acceder a los cursos (requiere autenticación)
@app.get("/cursos/", response_class=HTMLResponse, dependencies=[Depends(verify_token)])
async def read_index(request: Request):
    # Aquí puedes implementar la lógica para obtener los cursos desde la base de datos
    cursos = [{"nombre": "Curso de Python 1", "descripcion": "Introducción a Python"},
              {"nombre": "Curso de Python 2", "descripcion": "Avanzado de Python"}]

    # Si el token es válido y el usuario está autenticado, muestra la página de cursos
    return templates.TemplateResponse("cursos.html", {"request": request, "cursos": cursos})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)