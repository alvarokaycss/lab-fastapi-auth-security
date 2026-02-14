from fastapi import FastAPI

from core.settings import settings
from api.v1.api import router

app = FastAPI(title="Lab FastAPI Auth-Security")
app.include_router(router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD, log_level=settings.LOG_LEVEL)
