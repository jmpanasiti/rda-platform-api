from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from .api.middlewares.jwt_middlewares import JWTMiddlewares
from .api.routes import api_router
from .database import rda_db
from app.core.api_doc import api_description

api_middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=["renewed-token"],
    ),
    Middleware(JWTMiddlewares),
]
app = FastAPI(**api_description, middleware=api_middlewares)


app.include_router(api_router)


@app.on_event('startup')
async def startup_event():
    rda_db.connect()


@app.on_event('shutdown')
async def shutdown_event():
    rda_db.disconnect()
