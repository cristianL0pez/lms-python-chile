from pydantic import BaseModel

# Modelo de usuario
class User(BaseModel):
    id: str
    display_name: str
    email: str
    photo_url: str

# Modelo de curso
class Course(BaseModel):
    id: str
    title: str
    description: str
    instructor: str

# Modelo de datos para representar la estructura de userdata
class UserData(BaseModel):
    token: str
