from fastapi import FastAPI
from chesslib.parser import parse_pgn
from chesslib.engine import analyze_position, classify_move
from ai.llm import generate_commentary
from models import AnalyzeRequest, AnalyzeResponse

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# logging purposes
import logging
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    logger.info("Request received")
    start = time.time()
    
    positions = parse_pgn(request.pgn)
    results = []
    cp_before = 0
    
    for i, position in enumerate(positions):
        move_start = time.time()
        analysis = analyze_position(position["fen"])
        cp_after = analysis["evaluation"]["value"]
        
        classification, symbol = classify_move(
            position["board_before"],
            position["move"],
            cp_before,
            cp_after,
            analysis["top_moves"]
        )
        
        analysis["fen"] = position["fen"]
        analysis["classification"] = classification
        analysis["symbol"] = symbol
        results.append(analysis)
        cp_before = cp_after
        logger.info(f"Move {i+1} done in {time.time() - move_start:.2f}s")

    stockfish_done = time.time()
    logger.info(f"Stockfish total: {stockfish_done - start:.2f}s")

    commentaries, summary = generate_commentary(results)
    logger.info(f"LLM total: {time.time() - stockfish_done:.2f}s")

    for i in range(len(results)):
        results[i]["commentary"] = commentaries[i]
    
    logger.info(f"Request complete in {time.time() - start:.2f}s")
    return {"status": "ok", "analysis": results, "summary": summary}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)