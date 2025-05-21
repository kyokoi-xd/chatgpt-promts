from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/prompts")
def get_prompts(lang: str="ru"):
    filename = f"app/data/prompts_{lang}.json"
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
    
@app.get("/")
async def home(request: Request):
    try:
        lang = request.cookies.get("lang")
        agents_file = os.path.join(os.path.dirname(__file__), "data", "agents.json")
        with open(agents_file, "r", encoding="utf-8") as f:
            agents = json.load(f)
    except FileNotFoundError:
        agents = []

    prompts_file = os.path.join(os.path.dirname(__file__), "data", "prompts_ru.json") 
    with open(prompts_file, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    return templates.TemplateResponse("home.html", {
        "request": request, 
        "agents": agents, 
        "prompts": prompts, 
        "active_tab": "home"
        })