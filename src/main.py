from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends

from . import chatbot
from . import database as db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    path = ""
    global ai_assistant
    ai_assistant = chatbot.ChatBot(path)
    yield


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

templates = Jinja2Templates(directory="frontend")


def get_session():
    with db.Session(db.engine) as session:
        yield session

@app.get("/", response_class=HTMLResponse)
def main(session: Annotated[db.Session, Depends(get_session)]):
    with open("../frontend/ai_message.html") as AI:
        ai_message_template = AI.read()
    with open("../frontend/human_message.html") as HM:
        human_message_template = HM.read()
    # check chat mark

    message_history = []
    context = {"messages": message_history.join("")}

    return templates.TemplateResponse("chat_template.html", context)


@app.get("/get_response")
def get_response(message: str):
    default_response = ""
    result = {"response": ""}
    # check api protection

    flag: bool
    result = {"response": ""}
    if flag:
        result["response"] = default_response
    else:
        result["response"] = ai_assistant.respond(message)
    return result
