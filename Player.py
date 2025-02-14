
class Player:
    name = None # 姓名Str
    chess = None      # 棋子Str
    chess_dict = None
    epsilon = None
    value_rate = None

    def __init__(self, name, chess, epsilon=0.1, value_rate = 0.1):
        self.name = name
        self.chess = chess
        self.epsilon = epsilon
        self.value_rate = value_rate
    
    def set_q_table(self,q_table):
        self.chess_dict = q_table

    # def meke_game_move(self,current_board):
        
    