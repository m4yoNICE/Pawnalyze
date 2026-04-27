import chess.pgn

# recieves pgn from main.py
def get_pgn(pgn_string):
    pgn = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn)

def extract_pgn():
    #TODO: Extract every iteration of moves into FEN 
    print("extract")