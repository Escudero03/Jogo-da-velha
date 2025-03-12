from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Estado inicial do jogo
board = [""] * 9
current_player = "X"
scores = {"X": 0, "O": 0, "Empates": 0}
rounds = 0

def check_winner(board):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Linhas
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Colunas
        (0, 4, 8), (2, 4, 6)             # Diagonais
    ]
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    # Verifica empate
    if "" not in board:
        return "Empate"
    return None

@app.route("/")
def index():
    return render_template("index.html", board=board, scores=scores, rounds=rounds, player=current_player)

@app.route("/play", methods=["POST"])
def play():
    global current_player, board, scores, rounds
    position = int(request.form["position"])
    
    if board[position] == "":
        board[position] = current_player
        winner = check_winner(board)
        
        if winner:
            if winner == "Empate":
                scores["Empates"] += 1
            else:
                scores[winner] += 1
            rounds += 1
            return jsonify({"board": board, "winner": winner, "scores": scores, "rounds": rounds})
        
        current_player = "O" if current_player == "X" else "X"
    return jsonify({"board": board, "winner": None, "scores": scores, "rounds": rounds})

@app.route("/reset_round")
def reset_round():
    global board
    board = [""] * 9
    return jsonify({"board": board})

@app.route("/reset_all")
def reset_all():
    global board, scores, rounds, current_player
    board = [""] * 9
    scores = {"X": 0, "O": 0, "Empates": 0}
    rounds = 0
    current_player = "X"
    return jsonify({"board": board, "scores": scores, "rounds": rounds})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)