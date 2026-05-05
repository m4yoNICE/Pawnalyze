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

    # filter only highlighted moves
    highlighted = [
        (i, m) for i, m in enumerate(results)
        if m['classification'] in ["blunder", "mistake", "brilliant", "great"]
    ]

    commentaries = [""] * len(results)

    if highlighted:
        moves_text = ""
        for i, move in highlighted:
            eval_data = move['evaluation']
            val = eval_data['value']
            eval_str = f"+{val/100:.2f}" if eval_data['type'] == 'cp' else f"#{abs(val)}"
            moves_text += f"Move {i+1}: {move['best_move']} {eval_str} [{move['symbol']}]\n"

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"{persona}\n"
                            f"Analyze only the highlighted moves below. These are critical moments.\n"
                            "For each move: explain WHY it was a blunder/mistake/brilliant move. Reference board context.\n"
                            "2-3 sentences max per move. Tactical idea + consequence + coaching tip.\n"
                            "RAW JSON ONLY. Object with move numbers as keys. No markdown, no backticks."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Highlighted moves:\n{moves_text}\nReturn JSON object like {{\"1\": \"commentary\", \"5\": \"commentary\"}}"
                    }
                ]
            )
            text = response.choices[0].message.content.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            parsed = json.loads(text.strip())
            for i, _ in highlighted:
                commentaries[i] = parsed.get(str(i + 1), "[Commentary unavailable]")
        except Exception as e:
            print(f"ERROR: {e}")

    # generate overall summary
    summary = generate_summary(results, persona)
    return commentaries, summary


def generate_summary(results: list, persona: str):
    blunders = sum(1 for m in results if m['classification'] == 'blunder')
    mistakes = sum(1 for m in results if m['classification'] == 'mistake')
    brilliant = sum(1 for m in results if m['classification'] == 'brilliant')

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"{persona}\nWrite a 3-4 sentence overall game summary. Be honest about performance."
                },
                {
                    "role": "user",
                    "content": f"Game stats: {len(results)} moves, {blunders} blunders, {mistakes} mistakes, {brilliant} brilliant moves. Summarize the game."
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"SUMMARY ERROR: {e}")
        return "[Summary unavailable]"