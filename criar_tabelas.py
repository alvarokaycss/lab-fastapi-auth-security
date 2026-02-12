from core.settings import settings
from core.database import engine


async def create_tables():
    import models.__all_models

    print("Criando as tabelas no banco de dados...")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print("Tabelas criadas com sucesso!")


# O python em algumas versões não consegue criar tabelas em banco de dados
# sem essa configuração abaixo, mas em outras versões não precisa dela.
# Especificadamente no windows, essa configuração é necessária.
if __name__ == "__main__":
    import asyncio
    import platform

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(create_tables())
