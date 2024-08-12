from fastapi import FastAPI

from .database import models, common
from .routes import router


models.Base.metadata.create_all(bind=common.engine)
app = FastAPI()

app.include_router(router=router.router)
