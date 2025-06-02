from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def show_prompts(request: Request, lang: str = "ru"):
    filename = os.path.join(os.path.dirname(__file__), "data", f"prompts_{lang}.json")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            prompts = json.load(f)  
    except FileNotFoundError:
        prompts = {}

    return templates.TemplateResponse("prompts.html", {
        "request": request,
        "prompts": prompts,
        "lang": lang,
        "active_tab": "prompts",
    })

@app.get("/agents")
async def show_agents(request: Request):
    return templates.TemplateResponse("agents.html", {
        "request": request,
        "active_tab": "agents",
    })