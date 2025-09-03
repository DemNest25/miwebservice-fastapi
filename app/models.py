from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    correo     = Column(String(150), nullable=False, unique=True, index=True)
    password   = Column(String(100), nullable=False)  # guardaremos hash
    fecha_reg  = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
