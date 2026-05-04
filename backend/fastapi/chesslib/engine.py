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
    engine.set_fen_position(fen)

def get_best_move():
    return engine.get_best_move()

def get_evaluation():
    return engine.get_evaluation()

def get_top_moves():
    return engine.get_top_moves(3)

def eval_to_win_chance(cp):
    return 50 + 50 * (2 / (1 + 10 ** (-cp / 400)) - 1)

def classify_move(cp_before, cp_after, best_move, played_move):
    win_before = eval_to_win_chance(cp_before)
    win_after = eval_to_win_chance(cp_after)
    swing = win_before - win_after

    if swing > 15:
        return "??"
    elif swing > 5:
        return "?"
    elif swing > 2:
        return "?!"
    elif swing < -5:
        return "!!"
    elif swing < -2:
        return "!"
    return None 

# imported function
def analyze_position(fen):
    set_position(fen)
    return {
            "best_move": get_best_move(),
            "evaluation": get_evaluation(),
            "top_moves": get_top_moves()
        }
