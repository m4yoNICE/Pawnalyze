from dotenv import load_dotenv
from groq import Groq
import os
import random
import json
from ai.prompt import get_prompt

# load gen ai client with api key
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")
print(f"KEY LOADED: {api_key[:4]}...{api_key[-4:]}")  # debug line
client = Groq(api_key=api_key)

def generate_commentary(results: list):
    # styles = ["coach", "coach", "mommy", "tsun", "yunjin", "yuuka"]
    styles = ["mommy", "tsun", "yunjin", "yuuka"]
    style = random.choice(styles)

    prompt = get_prompt(style)
    moves_text = ""
    for i in range(len(results)):
        move = results[i]
        eval_data = move['evaluation']
        eval_str = f"{eval_data['type']}:{eval_data['value']}"
        moves_text += f"Move {i+1}: played={move['best_move']} eval={eval_str}\n"
    full_prompt = prompt + moves_text + "\nReturn ONLY a JSON array of strings, one per move. No markdown, no backticks, no explanation."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": prompt + "\nIMPORTANT: You must respond ONLY with a valid JSON array of strings. No apostrophes inside strings. Use proper chess commentary but avoid contractions like don't, it's, I'm, I've. No markdown, no backticks."
                },
                {
                    "role": "user",
                    "content": f"Analyze these moves and return exactly {len(results)} commentary strings as a JSON array:\n\n" + moves_text
                }
            ]
        )
        text = response.choices[0].message.content.strip()
        print(f"RAW RESPONSE: {text}")  # add this
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        parsed = json.loads(text.strip())
        while len(parsed) < len(results):
            parsed.append("[Commentary unavailable]")
        return parsed
    except Exception as e:
        print(f"ERROR: {e}")
        return ["[Commentary unavailable]"] * len(results)