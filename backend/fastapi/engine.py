from stockfish import Stockfish

engine = Stockfish(
    path="stockfish/stockfish-windows-x86-64-avx2.exe",
    depth=15,
    parameters={
        "Threads": 2,
        "Hash": 16,
        "Skill Level": 20
    }
)

def set_position(fen):
    return engine.set_fen_position(fen)

def get_best_move():
    return engine.get_best_move()

def get_evaluation():
    return engine.get_evaluation()

def get_top_moves():
    return engine.get_top_moves(3)