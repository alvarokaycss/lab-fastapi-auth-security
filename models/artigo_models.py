from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.settings import settings

class ArtigoModel(settings.DBBaseModel):
    __tablename__ = "artigos"
    
    id_artigo = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    url_fonte = Column(String(255))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    criador = relationship(
        "UsuarioModel", back_populates="artigos", lazy="joined"
    )    
