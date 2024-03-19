from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends

from . import chatbot
from . import database as db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    filename = "Indie Bites 9 PDF.pdf"
    global path
    path = f"media/{filename}"
    global ai_assistant
    ai_assistant = chatbot.ChatBot(f"{db.PATH.joinpath('media', filename)}")
    yield


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

templates = Jinja2Templates(directory="frontend")


def get_session():
    with db.Session(db.engine) as session:
        yield session


@app.get("/", response_class=HTMLResponse)
def main(request: Request, session: Annotated[db.Session, Depends(get_session)]):
    messages = db.read(session=session, data=db.MessageHistory)
    cutoff = db.read(
        session=session,
        data=db.NameSpace,
        query=[db.NameSpace.key == "chat-cutoff"],
        limit=1,
    )
    with open(f"{db.PATH.joinpath('frontend', 'ai_message.html')}") as AI:
        ai_message_template = AI.read()
    with open(f"{db.PATH.joinpath('frontend', 'human_message.html')}") as HM:
        human_message_template = HM.read()
    messages = messages[int(cutoff[0].value) :]
    result: list[str] = []
    for message in messages:
        template = (
            ai_message_template
            if message.sender.value == "ai"
            else human_message_template
        )
        result.append(
            template.replace(
                "${message}",
                f'<div class="chat-content">{message.message}</div>',
            )
        )
    context = {
        "request": request,
        "messages": "".join(result),
        "is_default_message": not bool(messages),
        "path": "true" if path else "false",
    }
    return templates.TemplateResponse("chat_template.html", context)


@app.get("/get_response")
def get_response(message: str, session: Annotated[db.Session, Depends(get_session)]):
    default_response = "This chatbot is currently turned off, the creator is broke and can no longer afford the price of the api key for the model :'(;_;, sponsor 0x65f38316d9a220d81a5EA4ee389b7f383796c276"
    result = {"response": ""}
    db_value = db.read(
        session=session,
        data=db.NameSpace,
        query=[db.NameSpace.key == "api-protection"],
        limit=1,
    )
    public = bool(db_value) and db_value[0].value == "true"
    if not public:
        result = {"response": default_response}
    else:
        result = {"response": ai_assistant.respond(message)}
    return result
