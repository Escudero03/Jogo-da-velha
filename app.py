from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Variáveis do jogo
board = [""] * 9
current_player = "X"
winner = None
rounds = 0
stats = {"Jogador 1": 0, "Jogador 2": 0, "Empates": 0}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    global board, current_player, winner, rounds, stats
    if winner:  # Se já houver vencedor, não faz nada
        return jsonify({"board": board, "winner": winner, "rounds": rounds, "stats": stats})

    index = int(request.form["index"])
    if board[index] == "":
        board[index] = current_player
        winner = check_winner()
        if winner:
            if winner == "X":
                stats["Jogador 1"] += 1
            else:
                stats["Jogador 2"] += 1
            rounds += 1
        elif "" not in board:
            winner = "Empate"
            stats["Empates"] += 1
            rounds += 1
        else:
            current_player = "O" if current_player == "X" else "X"

    return jsonify({"board": board, "winner": winner, "rounds": rounds, "stats": stats})

@app.route("/reset", methods=["POST"])
def reset():
    global board, current_player, winner
    board = [""] * 9
    current_player = "X"
    winner = None
    return jsonify({"board": board, "winner": winner, "rounds": rounds, "stats": stats})

@app.route("/reset_all", methods=["POST"])
def reset_all():
    global board, current_player, winner, rounds, stats
    board = [""] * 9
    current_player = "X"
    winner = None
    rounds = 0
    stats = {"Jogador 1": 0, "Jogador 2": 0, "Empates": 0}
    return jsonify({"board": board, "winner": winner, "rounds": rounds, "stats": stats})

def check_winner():
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != "":
            return board[condition[0]]
    return None

if __name__ == "__main__":
    app.run(debug=True)