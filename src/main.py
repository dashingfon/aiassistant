from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request, Response, Form, HTTPException, Body
from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends

from . import chatbot


@asynccontextmanager
async def lifespan(app: FastAPI):
    ...


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")


# def get_session():
#     with db.Session(db.engine) as session:
#         yield session