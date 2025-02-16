import hashlib
import random


def board_to_hash(board):
    flatten = ''.join(''.join(row) for row in board)
    hash_value = hashlib.md5(flatten.encode()).hexdigest()
    return hash_value


def is_three_in_a_row(board, move, chess):
    x, y = move
    # 检查坐标的有效性
    if x < 0 or x >= 3 or y < 0 or y >= 3:
        return False
    # 检查该位置是否为空
    current = board[x][y]
    if current != " ":
        return False

    # 定义需要检查的方向（行、列、主对角线、次对角线）
    directions = []
    # 行方向
    row = []
    for j in range(3):
        row.append((x, j, board[x][j]))
    directions.append(row)
    # 列方向
    column = []
    for i in range(3):
        column.append((i, y, board[i][y]))
    directions.append(column)
    # 主对角线（如果适用）
    if x == y:
        diagonal = []
        for i in range(3):
            diagonal.append((i, i, board[i][i]))
        directions.append(diagonal)
    # 次对角线（如果适用）
    if x + y == 2:
        diagonal_2 = []
        for i in range(3):
            diagonal_2.append((i, 2 - i, board[i][2 - i]))
        directions.append(diagonal_2)

    # 检查所有方向
    for cells in directions:
        count_x = 0
        count_blank = 0
        blank_pos = None
        for cell in cells:
            i, j, value = cell
            if value == chess:
                count_x += 1
            else:
                count_blank += 1
                blank_pos = (i, j)

        # 检查是否有两个相同的棋子和一个空格，并且空格的位置是移动坐标
        if count_blank == 1 and (count_x == 2 and blank_pos == move):
            return True
    return False

def is_two_in_a_row(board, move, chess):
    x, y = move
    # 检查坐标的有效性
    if x < 0 or x >= 3 or y < 0 or y >= 3:
        return False
    # 检查该位置是否为空
    current = board[x][y]
    if current != " ":
        return False

    # 定义需要检查的方向
    directions = []
    # 行方向
    row = board[x]
    directions.append(row)
    # 列方向
    column = [board[0][y], board[1][y], board[2][y]]
    directions.append(column)
    # 主对角线（如果适用）
    if x == y:
        diagonal = [board[0][0], board[1][1], board[2][2]]
        directions.append(diagonal)
    # 次对角线（如果适用）
    if x + y == 2:
        diagonal_2 = [board[0][2], board[1][1], board[2][0]]
        directions.append(diagonal_2)

    # 检查所有方向
    for cells in directions:
        count_x = cells.count(chess)
        count_blank = cells.count(" ")

        # 检查是否有一个相同的棋子和两个空白
        if count_x == 1 and count_blank == 2:
            return True
    return False


class Player:
    name = None  # 姓名Str
    chess = None  # 棋子Str
    chess_dict = {}
    epsilon = None  # 随即决策概率，0-1
    value_rate = None   # 学习率

    state_list = []

    def __init__(self, name, chess, epsilon=0.1, value_rate=0.1):
        self.name = name
        self.chess = chess
        self.epsilon = epsilon
        self.value_rate = value_rate

    def set_q_table(self, q_table):
        self.chess_dict = q_table

    # 计算学习棋局行动价值
    def count_state_list(self, is_win):
        if self.value_rate != 0:
            for i in range(len(self.state_list)):
                hash_board = board_to_hash(self.state_list[i]["board"])
                if hash_board not in self.chess_dict:
                    self.chess_dict[hash_board] = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (1, 0): 0, (1, 1): 0, (1, 2): 0,
                                                   (2, 0): 0, (2, 1): 0, (2, 2): 0}

                # 判断是否形成 “二连”
                is_good_operate = is_two_in_a_row(self.state_list[i]["board"], self.state_list[i]["operate"], self.chess)
                if is_good_operate:
                    self.chess_dict[hash_board][self.state_list[i]["operate"]] += 0.2 * self.value_rate

                # 判断是否形成“三连”
                is_good_operate_three = is_three_in_a_row(self.state_list[i]["board"], self.state_list[i]["operate"], self.chess)
                if is_good_operate_three:
                    self.chess_dict[hash_board][self.state_list[i]["operate"]] += 1 * self.value_rate

                # 胜利则奖励所有状态行动
                if is_win:
                    self.chess_dict[hash_board][self.state_list[i]["operate"]] += 0.4 * self.value_rate

    def reset_state_list(self):
        self.state_list = []

    def get_chess_dict(self):
        return self.chess_dict

    # 对局中根据学习到的数据，做出下棋决策
    def make_game_move(self, current_board, table_hash):
        # 获取空位置
        empty_indices = []
        for i in range(len(current_board)):
            for j in range(len(current_board[i])):
                if current_board[i][j] == " ":
                    empty_indices.append((i, j))

        if self.epsilon <= random.random():
            # 从价值表里取最高价值的
            if table_hash in self.chess_dict:
                filtered_dict = {k: v for k, v in self.chess_dict[table_hash].items() if k in empty_indices}
                max_index = max(filtered_dict, key=filtered_dict.get)
                self.state_list.append({"board": current_board, "operate": max_index})
                return max_index

        # 随机取一个
        random_index = random.choice(empty_indices)
        self.state_list.append({"board": current_board, "operate": random_index})
        return random_index

# if __name__ == '__main__':
#     a = is_three_in_a_row([["O","X","O"],
#                        ["O"," "," "],
#                        [" ","X","X"]],(0,1),"O")
#     print(a)
#     b = is_two_in_a_row([["O", " ", "O"],
#                            [" ", " ", "X"],
#                            ["X", "X", " "]], (0, 1), "O")
#     print(b)