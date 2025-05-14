import json
import os
import time
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("app/data/prompts_en.json", "r", encoding="utf-8") as f:
    prompts_en = json.load(f)

prompts_ru = []

for i, item in enumerate(prompts_en):
    act = item["act"]
    prompt = item["prompt"]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты переводчик с английского на русский язык. Переводи точно, понятно и адаптированно. Без пояснений."},
                {"role": "user", "content": f"Переведи на русский:\n\nАкт:\n{act}\n\nПромт:\n{prompt}"}
            ],
            temperature=0.3,
        )

        translated = response.choices[0].message.content

        parts = translated.split("Промт:")
        ru_act = parts[0].replace("Акт:", "").strip()
        ru_prompt = parts[1].strip() if len(parts) > 1 else ""

        prompts_ru.append({
            "act": ru_act,
            "prompt": ru_prompt
        })

        print(f"Translated {i + 1}/{len(prompts_en)}: {ru_act} -> {ru_prompt}")
        time.sleep(1.2)  # Sleep for 1 second to avoid hitting the rate limit

    except Exception as e:
        print(f"Error translating item {i + 1}: {e}")
        break

    with open("app/data/prompts_ru.json", "w", encoding="utf-8") as f:
        json.dump(prompts_ru, f, ensure_ascii=False, indent=2)

print("Translation completed and saved to prompts_ru.json")