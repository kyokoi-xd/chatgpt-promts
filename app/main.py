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
async def home(request: Request, lang: str="ru"):
    filename = os.path.join(os.path.dirname(__file__), "data", f"prompts_{lang}.json")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            prompts = json.load(f)
    except FileNotFoundError:
        prompts = []
    return templates.TemplateResponse("index.html", {"request": request, "prompts": prompts, "lang": lang})