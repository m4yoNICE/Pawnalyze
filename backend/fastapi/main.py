from fastapi import FastAPI
from chesslib.parser import parse_pgn
from chesslib.engine import analyze_position
from chesslib.engine import analyze_position, classify_move
from ai.llm import generate_commentary
from models import AnalyzeRequest, AnalyzeResponse

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

app = FastAPI()

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    fens = parse_pgn(request.pgn)
    results = []
    cp_before = 0
    # loop through each move position to stockfish and groyp them as one
    for fen in fens:
        analysis = analyze_position(fen)
        cp_after = analysis["evaluation"]["value"]
        best_move = analysis["best_move"]

        analysis["fen"] = fen  
        analysis["classification"] = classify_move(cp_before, cp_after, best_move, best_move)
        results.append(analysis)

    # batch call everyone to llm in a single prompt
    commentaries = generate_commentary(results)

    # add commentaries to the batch
    for i in range(len(results)):
        results[i]["commentary"] = commentaries[i]
        
    return {"status": "ok", "analysis": results}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)