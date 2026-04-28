from fastapi import FastAPI
from parser import parse_pgn
from engine import analyze_position
from models import AnalyzeRequest, AnalyzeResponse
from llm import generate_commentary

app = FastAPI()

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    fens = parse_pgn(request.pgn)
    results = []
    # loop through each move position and llm results
    for fen in fens:
        analysis = analyze_position(fen)
        commentary = generate_commentary(
            fen,
            analysis["best_move"],
            analysis["evaluation"],
            analysis["top_moves"]
        )
        analysis["commentary"] = commentary
        analysis["fen"] = fen
        results.append(analysis)

    return {"status": "ok", "analysis": results}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)