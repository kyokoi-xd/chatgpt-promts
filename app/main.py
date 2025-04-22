from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/promts")
def get_promts(lang: str="ru"):
    filename = f"app/data/promts_{lang}.json"
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
    