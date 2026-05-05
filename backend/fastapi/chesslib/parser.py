import chess.pgn
import io

# recieves pgn from main.py
def parse_pgn(pgn_string):
    pgn = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn)
    return iterate_moves(game)

def iterate_moves(game):
    board = game.board()
    positions = []
    for move in game.mainline_moves():
        board_before = board.copy()
        board.push(move)
        positions.append({
            "fen": board.fen(),
            "move": move,
            "board_before": board_before
        })
    return positions


