import Player
import json
from TicGame import TicTacToe

def save_q_table(q_table, file_path="q_table.json"):
    with open(file_path, "w") as f:
        json.dump(q_table, f, indent=4, ensure_ascii=False)

def load_q_table(file_path="q_table.json"):
    try:
         with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def Rl():
    '''
    q_entry = {
        "q_value_x": 0.8,
        "q_value_o": -0.5
    }
    q_table[state_hash] = q_entry
    '''
    
    player1 = Player("pyf","X")#棋子只能为O或X
    player1.set_q_table(load_q_table("q_table1.json"))

    player2 = Player("wmm","O")
    player2.set_q_table(load_q_table("q_table2.json"))

    game = TicTacToe(player1,player2)
    while True:
        step_player = game.get_current_player()
        
