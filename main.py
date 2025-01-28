# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db_routes import router

app = FastAPI()

# Lista de orígenes permitidos (por ejemplo, tus dominios frontend)
origins = [
    "http://localhost:3000",  # Si tu frontend está corriendo en este puerto
    "https://mi-frontend.com",  # Otro dominio permitido
]

# Configuración del middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)


# Registrar los endpoints en la aplicación FastAPI
app.include_router(router)

# Esto se puede usar para configurar la aplicación o la documentación
@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API!"}


# uvicorn main:app --reload
