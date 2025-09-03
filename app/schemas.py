from pydantic import BaseModel, EmailStr, Field

class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    correo: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, max_length=100)

class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=100)
    correo: EmailStr | None = None
    password: str | None = Field(None, min_length=6, max_length=100)

class UsuarioOut(UsuarioBase):
    id_usuario: int

    class Config:
        from_attributes = True
