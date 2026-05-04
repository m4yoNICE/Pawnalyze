from dotenv import load_dotenv
from groq import Groq
import os
import random
import json
from ai.prompt import get_prompt

load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")
print(f"KEY LOADED: {api_key[:4]}...{api_key[-4:]}")
client = Groq(api_key=api_key)

def generate_commentary(results: list):
    styles = ["mommy", "tsun", "yunjin", "yuuka"]
    style = random.choice(styles)
    persona = get_prompt(style)

    moves_text = ""
    for i in range(len(results)):
        move = results[i]
        eval_data = move['evaluation']
        val = eval_data['value']
        eval_str = f"+{val/100:.2f}" if eval_data['type'] == 'cp' else f"#{abs(val)}"
        moves_text += f"{i+1}.{move['best_move']} {eval_str} [{move['classification']}]\n"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"{persona}\n"
                        f"You are analyzing a full chess game of {len(results)} moves.\n"
                        "Write rich, contextual commentary — reference earlier moves when relevant, identify patterns, explain WHY each move is good or bad, not just what happened.\n"
                        "Each commentary: 2-3 sentences. Tactical idea + positional consequence + coaching insight.\n"
                        "RAW JSON ONLY. Array of exactly N strings. No markdown, no backticks, no contractions."
                    )
                },
                {
                    "role": "user",
                    "content": f"This is a complete game. Return ONE JSON array of exactly {len(results)} strings.\n\nGame moves:\n{moves_text}"
                }
            ]
        )
        text = response.choices[0].message.content.strip()
        print(f"RAW RESPONSE: {text}")
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