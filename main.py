from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import models  # noqa: F401  (enregistre les tables)
from controllers.user_controller import router as user_router
from core.exceptions import ConflictException, NotFoundException
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Users API")


@app.exception_handler(NotFoundException)
def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(ConflictException)
def conflict_handler(request: Request, exc: ConflictException):
    return JSONResponse(status_code=409, content={"detail": exc.message})


app.include_router(user_router)