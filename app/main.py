from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

UI_TEXT ={
    "ru" : {
        "nav_prompts": "Промты",
        "nav_agents": "ИИ-агенты (в разработке)",
        "header_title": "Готовые промты",
        "header_subtitle": "Выбирай, копируй и используй — на русском или английском",
        "search_placeholder": "Поиск по названию или тексту...",
        "show_more": "Показать ещё",
        "prompt_copied": "Промт скопирован.",
        "expand_prompt": "Читать полностью",
    },
    "en": {
        "nav_prompts": "Prompts",
        "nav_agents": "AI Agents (in development)",
        "header_title": "Ready-made prompts",
        "header_subtitle": "Choose, copy and use — in Russian or English",
        "search_placeholder": "Search by title or text...",
        "show_more": "Show more",
        "prompt_copied": "Prompt copied.",
        "expand_prompt": "Read more",
    }
}

@app.get("/")
async def show_prompts(request: Request, lang: str = "ru"):
    dir_path = os.path.dirname(__file__)
    file_ru = os.path.join(dir_path, "data", f"prompts_ru.json")
    file_en = os.path.join(dir_path, "data", f"prompts_en.json")
    try:
        with open(file_ru, "r", encoding="utf-8") as f:
            prompts_ru = json.load(f)
    except FileNotFoundError:
        prompts_ru = []

    try:
        with open(file_en, "r", encoding="utf-8") as f:
            prompts_en = json.load(f)
    except FileNotFoundError:
        prompts_en = []

    combined = []
    length = min(len(prompts_ru), len(prompts_en))
    for i in range(length):
        combined.append({
            "act_ru": prompts_ru[i].get("act", ""),
            "prompt_ru": prompts_ru[i].get("prompt", ""),
            "act_en": prompts_en[i].get("act", ""),
            "prompt_en": prompts_en[i].get("prompt", ""),
        })

    ui = UI_TEXT.get(lang, UI_TEXT["ru"])

    return templates.TemplateResponse("prompts.html", {
        "request": request,
        "prompts": combined,
        "lang": lang,
        "active_tab": "prompts",
        "ui": ui,
        "active_lang": lang,
    })

@app.get("/agents")
async def show_agents(request: Request, lang: str = "ru"):
    ui = UI_TEXT.get(lang, UI_TEXT["ru"])
    return templates.TemplateResponse("agents.html", {
        "request": request,
        "active_tab": "agents",
        "lang": lang,
        "ui": ui,
        "active_lang": lang,
    })