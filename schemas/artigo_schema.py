from pydantic import BaseModel as SCBaseModel
from pydantic import ConfigDict
from pydantic import HttpUrl

from typing import Optional

class ArtigoSchema(SCBaseModel):
    id_artigo: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    id_usuario: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
