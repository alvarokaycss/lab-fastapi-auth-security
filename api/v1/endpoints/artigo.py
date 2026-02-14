from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.artigo_models import ArtigoModel
from models.usuario_models import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from schemas.usuario_schema import UsuarioSchemaArtigos

from core.deps import get_session, get_current_user

router: APIRouter = APIRouter(prefix="/artigos", tags=["Artigos"])


# GET Artigos
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ArtigoSchema])
async def get_artigos(
    db: AsyncSession = Depends(get_session),
):
    query = select(ArtigoModel)
    result = await db.execute(query)
    artigos = result.scalars().unique().all()
    return artigos


# GET Artigo
@router.get("/{id_artigo}", status_code=status.HTTP_200_OK, response_model=ArtigoSchema)
async def get_artigo(id_artigo: int, db: AsyncSession = Depends(get_session)):
    query = select(ArtigoModel).where(ArtigoModel.id_artigo == id_artigo)
    result = await db.execute(query)
    artigo = result.scalars().one_or_none()

    if not artigo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado"
        )
    return artigo


# POST Artigo
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(
    artigo: ArtigoSchema,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    novo_artigo: ArtigoModel = ArtigoModel(
        **artigo.model_dump(), id_usuario=current_user.id_usuario
    )
    db.add(novo_artigo)

    try:
        await db.commit()
        await db.refresh(novo_artigo)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade ao criar artigo",
        )
    return novo_artigo


# PUT Artigo
@router.put("/{id_artigo}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def put_artigo(
    id_artigo: int,
    artigo: ArtigoSchema,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    query = select(ArtigoModel).where(ArtigoModel.id_artigo == id_artigo)
    result = await db.execute(query)
    artigo_atual = result.scalars().one_or_none()

    if not artigo_atual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado"
        )

    if artigo_atual.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para editar este artigo",
        )

    for campo, valor in artigo.model_dump(exclude={"id_usuario", "id_artigo"}).items():
        setattr(artigo_atual, campo, valor)

    try:
        await db.commit()
        await db.refresh(artigo_atual)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade ao atualizar artigo",
        )

    return artigo_atual


# DELETE Artigo
@router.delete("/{id_artigo}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(
    id_artigo: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    query = select(ArtigoModel).where(ArtigoModel.id_artigo == id_artigo)
    result = await db.execute(query)
    artigo_atual = result.scalars().one_or_none()

    if not artigo_atual:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado"
        )

    if artigo_atual.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar este artigo",
        )

    try:
        await db.delete(artigo_atual)
        await db.commit()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro de integridade ao deletar artigo",
        )

    return
