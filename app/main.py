from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas, crud, models

app = FastAPI(
    title="Mi WebService",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS: abre para pruebas (ajusta dominios en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"success": True, "message": "OK"}

@app.get("/api", include_in_schema=False)
def index():
    return {
        "success": True,
        "message": "Servicio activo",
        "data": {
            "env": "production",
            "docs": "/api/docs",
            "endpoints": ["/api/health", "/api/usuarios"]
        }
    }

# CRUD Usuarios
@app.get("/api/usuarios", response_model=list[schemas.UsuarioOut])
def get_usuarios(db: Session = Depends(get_db)):
    return crud.listar_usuarios(db)

@app.get("/api/usuarios/{id_usuario}", response_model=schemas.UsuarioOut)
def get_usuario(id_usuario: int, db: Session = Depends(get_db)):
    obj = crud.obtener_usuario(db, id_usuario)
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obj

@app.post("/api/usuarios", response_model=schemas.UsuarioOut, status_code=201)
def post_usuario(data: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Validar correo único
    existentes = [u for u in crud.listar_usuarios(db) if u.correo.lower() == data.correo.lower()]
    if existentes:
        raise HTTPException(status_code=409, detail="El correo ya existe")
    return crud.crear_usuario(db, data)

@app.put("/api/usuarios/{id_usuario}", response_model=schemas.UsuarioOut)
def put_usuario(id_usuario: int, data: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    if data.correo:
        # Verificar unicidad si cambia correo
        todos = crud.listar_usuarios(db)
        conflicto = [u for u in todos if u.correo.lower() == data.correo.lower() and u.id_usuario != id_usuario]
        if conflicto:
            raise HTTPException(status_code=409, detail="El correo ya existe")
    obj = crud.actualizar_usuario(db, id_usuario, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obj

@app.delete("/api/usuarios/{id_usuario}", status_code=204)
def delete_usuario(id_usuario: int, db: Session = Depends(get_db)):
    ok = crud.eliminar_usuario(db, id_usuario)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return
