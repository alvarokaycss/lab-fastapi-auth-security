from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.settings import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=True)
    sobrenome = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    admin = Column(Boolean, default=False)
    artigos = relationship(
        "ArtigoModel", back_populates="criador", lazy="joined",
        cascade="all, delete-orphan", uselist=True
    )
