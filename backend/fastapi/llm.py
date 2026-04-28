from dotenv import load_dotenv
from google import genai
import os
import random
from prompt import get_prompt

# load gen ai client with api key
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")
print(f"KEY LOADED: {api_key[:4]}...{api_key[-4:]}")  # debug line
client = genai.Client(api_key=api_key)


def generate_commentary(fen, best_move, evaluation, top_move):
    styles = ["coach", "coach", "mommy", "tsun", "yunjin", "yuuka"]
    style = random.choice(styles)

    prompt = get_prompt(style)

    full_prompt = prompt + f"""
        FEN: {fen}
        Best move: {best_move}
        Evaluation: {evaluation}
        Top move: {top_move}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        return f"[Commentary unavailable: {str(e)[:50]}]"