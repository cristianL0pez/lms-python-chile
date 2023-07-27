from fastapi import FastAPI, Request, Depends, HTTPException, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import credentials , auth
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from .models import User as User_model
from .schema import User as User_schema
from dotenv import load_dotenv
from datetime import datetime 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi import Body
from typing import Optional
from pydantic import BaseModel, AnyHttpUrl, HttpUrl, constr, validator



app = FastAPI()




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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))



# Endpoint para iniciar sesión con Firebase
@app.post("/login", response_model=User_schema)
async def login_firebase(user:User_schema):
    try:
        decoded_token = auth.verify_id_token(User_schema.token)
        user = User_model(
            uid=decoded_token['uid'],
            displayName=decoded_token.get('name', ''),
            email=decoded_token.get('email', ''),
            photoURL=decoded_token.get('picture', '')
        )
        # Guardar los datos del usuario en la base de datos
        with db():
            db_user = db.session.query(User_model).filter(User_model.uid == user.uid).first()
            if not db_user:
                db.session.add(user)
                db.session.commit()
            else:
                # Si el usuario ya existe en la base de datos, actualiza sus datos
                db_user.displayName = user.displayName
                db_user.email = user.email
                db_user.photoURL = user.photoURL
                db.session.commit()
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token de Firebase inválido")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)