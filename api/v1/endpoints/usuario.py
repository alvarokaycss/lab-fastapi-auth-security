from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.usuario_models import UsuarioModel
from schemas.usuario_schema import (
    UsuarioSchema,
    UsuarioSchemaArtigos,
    UsuarioSchemaCreate,
    UsuarioSchemaUpdate,
)
from core.deps import get_session, get_current_user
from core.auth import autenticar_usuario, criar_token_acesso
from core.security import hash_password


router: APIRouter = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# GET Logado
@router.get("/logado", response_model=UsuarioSchema)
async def get_logado(current_user: UsuarioModel = Depends(get_current_user)):
    return current_user


# POST Sign Up
@router.post(
    "/signup", response_model=UsuarioSchema, status_code=status.HTTP_201_CREATED
)
async def signup(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        **usuario.model_dump(exclude={"senha"}), senha=hash_password(usuario.senha)
    )
    db.add(novo_usuario)

    try:
        await db.commit()
        await db.refresh(novo_usuario)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade ao criar usuário",
        )
    return novo_usuario


# POST Login
@router.post("/login", response_model=UsuarioSchema, status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    usuario = await autenticar_usuario(
        email=form_data.username, senha=form_data.password, db=db
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Credenciais inválidas"
        )

    token_acesso = criar_token_acesso(sub=usuario.id_usuario)
    return JSONResponse(content={"access_token": token_acesso, "token_type": "bearer"})


# GET Usuarios
@router.get("/", response_model=List[UsuarioSchema], status_code=status.HTTP_200_OK)
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    query = select(UsuarioModel)
    result = await db.execute(query)
    usuarios: List[UsuarioModel] = result.scalars().unique().all()
    return usuarios


# GET Usuario
@router.get(
    "/{id_usuario}", response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK
)
async def get_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    query = select(UsuarioModel).where(UsuarioModel.id_usuario == id_usuario)
    result = await db.execute(query)
    usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    return usuario


# PUT Usuario
@router.put(
    "/{id_usuario}", response_model=UsuarioSchema, status_code=status.HTTP_200_OK
)
async def put_usuario(
    id_usuario: int,
    usuario: UsuarioSchemaUpdate,
    db: AsyncSession = Depends(get_session),
):
    query = select(UsuarioModel).where(UsuarioModel.id_usuario == id_usuario)
    result = await db.execute(query)
    usuario_atual: UsuarioModel = result.scalars().unique().one_or_none()

    if not usuario_atual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )

    dados_update = usuario.model_dump(exclude_unset=True)

    if "senha" in dados_update:
        dados_update["senha"] = hash_password(dados_update["senha"])

    for campo, valor in dados_update.items():
        setattr(usuario_atual, campo, valor)

    try:
        await db.commit()
        await db.refresh(usuario_atual)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade ao atualizar usuário",
        )
    return usuario_atual


# DELETE Usuario
@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id_usuario: int, db: AsyncSession = Depends(get_session)):
    query = select(UsuarioModel).where(UsuarioModel.id_usuario == id_usuario)
    result = await db.execute(query)
    usuario: UsuarioModel = result.scalars().unique().one_or_none()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    await db.delete(usuario)
    await db.commit()
    return
