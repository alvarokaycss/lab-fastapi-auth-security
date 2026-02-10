from pydantic import BaseModel as SCBaseModel
from pydantic import ConfigDict, EmailStr

from typing import List, Optional

from schemas.artigo_schema import ArtigoSchema


class UsuarioSchema(SCBaseModel):
    id_usuario: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool
    
    model_config = ConfigDict(from_attributes=True)


class UsuarioSchemaCreate(UsuarioSchema):
    senha: str


class UsuarioSchemaArtigos(UsuarioSchema):
    artigos: Optional[List[ArtigoSchema]]
    

class UsuarioSchemaUpdate(UsuarioSchema):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    admin: Optional[bool] = None
    