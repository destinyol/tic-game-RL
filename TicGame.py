import random
import Player
import hashlib


class TicTacToe:

    player1 = None
    player2 = None
    current_player = None

    def __init__(self, player1, player2):
        """
        初始化游戏

        参数:
        - player1: 玩家1（player类实例）
        - player2: 玩家2（player类实例）
        """
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.current_player = random.choice([player1, player2])  # 随机选择先手玩家
        self.winner = None  # 胜利者（初始为 None）
        self.game_over = False  # 游戏是否结束
        self.player1 = player1
        self.player2 = player2

    def re_play_game(self):
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.current_player = random.choice([self.player1, self.player2])  # 随机选择先手玩家
        self.winner = None  # 胜利者（初始为 None）
        self.game_over = False  # 游戏是否结束

    def get_current_player(self):
        """
        获取当前玩家

        返回值:
        - 当前玩家的player对象
        """
        return self.current_player

    def make_move(self, row, col):
        """
        玩家走一步棋

        参数:
        - row: 行号（0-2）
        - col: 列号（0-2）

        返回值:
        - True 表示下棋成功，False 表示失败（例如位置无效或已占用）
        """
        if self.game_over:
            return False  # 游戏已结束，无法下棋

        # 检查输入合法性
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False

        if self.board[row][col] != " ":
            return False  # 位置已被占用

        # 更新棋盘
        self.board[row][col] = self.current_player.chess
        # 检查游戏是否结束
        self.check_game_over()

        # 切换玩家
        if not self.game_over:
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

        return True

    def get_board_state(self):
        """
        返回棋局当前状态

        返回值:
        - 当前棋盘状态（二维数组）
        """
        return [row.copy() for row in self.board]

    def check_game_over(self):
        """
        检查游戏是否结束，并设置胜利者或平局
        """
        # 检查行
        for row in self.board:
            if all(cell == row[0] and cell != " " for cell in row):
                self.winner = self.current_player
                self.game_over = True
                return

        # 检查列
        for col in range(3):
            if all(self.board[row][col] == self.board[0][col] and self.board[0][col] != " " for row in range(3)):
                self.winner = self.current_player
                self.game_over = True
                return

        # 检查对角线
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            self.winner = self.current_player
            self.game_over = True
            return

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            self.winner = self.current_player
            self.game_over = True
            return

        # 检查平局
        if all(cell != " " for row in self.board for cell in row):
            self.game_over = True

    def get_winner(self):
        """
        获取胜利玩家的player对象

        返回值:
        - 胜利玩家的player对象，若游戏未结束则返回 None
        """
        return self.winner

    def is_game_over(self):
        """
        判断游戏是否结束

        返回值:
        - True 表示游戏结束，False 表示未结束
        """
        return self.game_over

    def print_board(self):
        """
        打印当前棋盘状态
        """
        for row in self.board:
            print(" | ".join(row))
            print("---------")

    def get_table_hash(self):
        '''
        将棋盘状态变为唯一hash值，便于存储比对
        '''
        flatten = ''.join(''.join(row) for row in self.board)
        hash_value = hashlib.md5(flatten.encode()).hexdigest()
        return hash_value


# 示例用法
if __name__ == "__main__":
    # 创建玩家
    player1 = Player("Alice", "X")
    player2 = Player("Bob", "O")

    # 初始化游戏
    game = TicTacToe(player1, player2)
    print(f"先手玩家是：{game.get_current_player().name} ({game.get_current_player().chess})")

    # 模拟玩家下棋
    game.print_board()
    while not game.is_game_over():
        current_player = game.get_current_player()
        try:
            move = input(f"玩家 {current_player.name} 的回合，请输入行号和列号（如：0 0）：")
            row, col = map(int, move.split())
        except:
            print("无效输入，请输入两个整数（例如：0 0）！")
            continue

        if game.make_move(row, col):
            game.print_board()
        else:
            print("无效的移动，请重新输入！")

    # 游戏结束
    winner = game.get_winner()
    if winner:
        print(f"玩家 {winner.name} 获胜！")
    else:
        print("游戏平局！")
