
import os
import pickle
import time
from Player import Player
from TicGame import TicTacToe


def save_q_table(q_table, file_path="q_table1.pkl"):
    with open(file_path, "wb") as f:
        pickle.dump(q_table, f)

def load_q_table(file_path="q_table1.pkl"):
    if not os.path.exists(file_path):
        # 如果文件不存在，创建一个空的 Q 表
        empty_q_table = {}
        save_q_table(empty_q_table, file_path)
        return empty_q_table
    else:
        try:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        except EOFError:
            return {}


def Rl(times,debug_mode=False):
    debug = debug_mode

    start_time = time.time()

    player1 = Player("pyf", "X",0.1,0.1)  # 棋子只能为O或X  epsilon是随即决策概率，即探索率；value_rate是学习率，为0则不学了
    player1.set_q_table(load_q_table("q_table1.pkl"))

    player2 = Player("wmm", "O",1,0)
    player2.set_q_table(load_q_table("q_table2.pkl"))

    game = TicTacToe(player1, player2)

    game_res = {player1.name: 0, player2.name: 0, "平局": 0}

    # print(player1.get_chess_dict())

    for i in range(times):

        if debug:
            print("对局开始=============================================================")
        while True:
            # 当前player
            step_player = game.get_current_player()

            # 做出选择
            choice = step_player.make_game_move(game.get_board_state(), game.get_table_hash())
            if debug:
                game.print_board()
                print(step_player.name+" 棋子:"+step_player.chess+",这一步做出的决定为:")
                print(choice)
            game.make_move(choice[0], choice[1])
            game.check_game_over()
            if game.is_game_over():
                break

        winner = game.get_winner()
        if winner != None:
            if debug:
                print("赢家为" + winner.name)
            player1.count_state_list(winner.name == player1.name, player2.chess)
            player2.count_state_list(winner.name == player2.name, player1.chess)
            game_res[winner.name] += 1
        else:
            if debug:
                print("平局")
            player1.count_state_list(None, player2.chess)
            player2.count_state_list(None, player1.chess)
            game_res["平局"] += 1
        player1.reset_state_list()
        player2.reset_state_list()

        # print("=============================")
        # game.print_board()

        game.re_play_game()

    save_q_table(player1.get_chess_dict(), "q_table1.pkl")
    save_q_table(player2.get_chess_dict(), "q_table2.pkl")
    print("训练结束，输赢结果为：")
    print(game_res)

    end_time = time.time()
    # 计算运行时间（单位：秒）
    elapsed_time = end_time - start_time
    print(f"运行时间：{elapsed_time:.6f} 秒")
