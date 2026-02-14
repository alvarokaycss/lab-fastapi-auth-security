from fastapi import APIRouter
from api.v1.endpoints import artigo
from api.v1.endpoints import usuario

router = APIRouter()

router.include_router(usuario.router)
router.include_router(artigo.router)
