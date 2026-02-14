from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario_models import UsuarioModel
from core.settings import settings
from core.security import verify_password

from pydantic import EmailStr


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuarios/login")


async def autenticar_usuario(
    email: EmailStr, senha: str, db: AsyncSession
) -> Optional[UsuarioModel]:
    query = select(UsuarioModel).filter(UsuarioModel.email == email)
    result = await db.execute(query)
    usuario: UsuarioModel = result.unique().scalars().one_or_none()

    if not usuario:
        return None

    if not verify_password(senha, usuario.senha):
        return None

    return usuario


def _criar_token_jwt(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1
    # Seguimos a RFC 7519 para criar o token JWT
    payload = {}

    fuso_horario = ZoneInfo("America/Sao_Paulo")
    expira_em = datetime.now(tz=fuso_horario) + tempo_vida

    payload["type"] = tipo_token  # tipo do token
    payload["exp"] = expira_em  # data de expiração do token
    payload["sub"] = str(sub)  # subject
    payload["iat"] = datetime.now(tz=fuso_horario)  # data de criação do token

    token = jwt.encode(payload, key=settings.JWT_SECRET, algorithm=settings.ALGORITHM)
    return token


def criar_token_acesso(sub: str) -> str:
    return _criar_token_jwt(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
