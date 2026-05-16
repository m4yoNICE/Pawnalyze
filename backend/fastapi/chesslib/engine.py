from stockfish import Stockfish
import chess
import math

engine = Stockfish(
    path="stockfish/stockfish-windows-x86-64-avx2.exe",
    depth=10,
    parameters={
        "Threads": 4,
        "Hash": 128,
        "Skill Level": 20
    }
)

def set_position(fen):
    engine.set_fen_position(fen)

def get_top_moves():
    return engine.get_top_moves(3)

# Material values for sacrifice detection
PIECE_VALUES = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}

def get_material_score(board, color):
    return sum(len(board.pieces(pt, color)) * val for pt, val in PIECE_VALUES.items())

# Lichess-aligned win probability formula
def cp_to_win_prob(cp):
    if cp is None:
        return 0.5
    return (50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)) / 100

def classify_move(board_before, move, cp_before, cp_after, top_moves):
    # 1. Calculate Expected Points (EP)
    ep_before = cp_to_win_prob(cp_before)
    ep_after = cp_to_win_prob(cp_after)
    ep_loss = max(0, ep_before - ep_after)

    # 2. Check for "Only Move" (Great Move !)
    # If the gap between 1st and 2nd best move is huge (> 0.15 EP)
    if len(top_moves) > 1:
        best_ep = cp_to_win_prob(top_moves[0].get('Centipawn') or 0)
        second_best_ep = cp_to_win_prob(top_moves[1].get('Centipawn') or 0)
        if best_ep - second_best_ep > 0.15 and ep_loss < 0.02:
            return "great", "!"

    # 3. Check for Sacrifice (Brilliant Move !!)
    # Logic: Material went down, but win prob stayed high
    mat_before = get_material_score(board_before, board_before.turn)

    board_after = board_before.copy()
    board_after.push(move)
    # Opponent might have taken something
    mat_after = get_material_score(board_after, board_before.turn)

    if mat_after < mat_before and ep_loss < 0.02:
        # Don't call it brilliant if we are already crushing (+5.0 or 0.95 EP)
        if ep_before < 0.95:
            return "brilliant", "!!"

    # 4. Standard Classifications (Lichess-aligned thresholds)
    if ep_loss >= 0.20: return "blunder", "??"
    if ep_loss >= 0.10: return "mistake", "?"
    if ep_loss >= 0.05: return "inaccuracy", "?!"
    if ep_loss < 0.02: return "best", ""

    return "good", ""

# imported function — consolidates 3 Stockfish calls into 1
def analyze_position(fen):
    set_position(fen)
    top_moves = get_top_moves()

    best_move = top_moves[0]["Move"] if top_moves else None
    evaluation = {
        "type": "cp" if top_moves[0]["Centipawn"] is not None else "mate",
        "value": top_moves[0]["Centipawn"] if top_moves[0]["Centipawn"] is not None else top_moves[0]["Mate"]
    } if top_moves else {"type": "cp", "value": 0}

    return {
        "best_move": best_move,
        "evaluation": evaluation,
        "top_moves": top_moves
    }