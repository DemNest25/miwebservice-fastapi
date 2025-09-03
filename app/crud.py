from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.hash import bcrypt
from . import models, schemas

def listar_usuarios(db: Session) -> list[models.Usuario]:
    stmt = select(models.Usuario).order_by(models.Usuario.id_usuario)
    return db.execute(stmt).scalars().all()

def obtener_usuario(db: Session, id_usuario: int) -> models.Usuario | None:
    return db.get(models.Usuario, id_usuario)

def crear_usuario(db: Session, data: schemas.UsuarioCreate) -> models.Usuario:
    # Hash de contraseña
    hashed = bcrypt.hash(data.password)
    obj = models.Usuario(
        nombre=data.nombre,
        correo=data.correo,
        password=hashed
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def actualizar_usuario(db: Session, id_usuario: int, data: schemas.UsuarioUpdate) -> models.Usuario | None:
    obj = db.get(models.Usuario, id_usuario)
    if not obj:
        return None
    if data.nombre is not None:
        obj.nombre = data.nombre
    if data.correo is not None:
        obj.correo = data.correo
    if data.password is not None:
        obj.password = bcrypt.hash(data.password)
    db.commit()
    db.refresh(obj)
    return obj

def eliminar_usuario(db: Session, id_usuario: int) -> bool:
    obj = db.get(models.Usuario, id_usuario)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
