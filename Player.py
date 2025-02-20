import copy
import hashlib
import random


def find_win_move(board, move_point, chess):
    copy_board = copy.deepcopy(board)
    copy_board[move_point[0]][move_point[1]] = " "
    # 检查每一行
    for i in range(3):
        row = copy_board[i]
        if row.count(chess) == 2 and row.count(" ") == 1:
            empty_col = row.index(" ")
            return (i, empty_col)

    # 检查每一列
    for j in range(3):
        column = [copy_board[0][j], copy_board[1][j], copy_board[2][j]]
        if column.count(chess) == 2 and column.count(" ") == 1:
            empty_row = [i for i in range(3) if copy_board[i][j] == " "][0]
            return (empty_row, j)

    # 检查主对角线 (0,0), (1,1), (2,2)
    diag = [copy_board[0][0], copy_board[1][1], copy_board[2][2]]
    if diag.count(chess) == 2 and diag.count(" ") == 1:
        empty_index = diag.index(" ")
        return (empty_index, empty_index)

    # 检查副对角线 (0,2), (1,1), (2,0)
    anti_diag = [copy_board[0][2], copy_board[1][1], copy_board[2][0]]
    if anti_diag.count(chess) == 2 and anti_diag.count(" ") == 1:
        empty_index = anti_diag.index(" ")
        if empty_index == 0:
            return (0, 2)
        elif empty_index == 1:
            return (1, 1)
        else:
            return (2, 0)

    # 如果没有找到获胜位置
    return None

def board_to_hash(board):
    flatten = ''.join(''.join(row) for row in board)
    hash_value = hashlib.md5(flatten.encode()).hexdigest()
    return hash_value


def is_three_in_a_row(origin_board, move, chess):
    board = copy.deepcopy(origin_board)
    board[move[0]][move[1]] = " "

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

def is_two_in_a_row(origin_board, move, chess):
    board = copy.deepcopy(origin_board)
    board[move[0]][move[1]] = " "

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

    # # 计算学习棋局行动价值
    # def count_state_list(self, is_win, the_other_chess):
    #     if self.value_rate != 0:
    #         step = 0
    #         for i in range(len(self.state_list)):
    #             step += 1

    #             hash_board = board_to_hash(self.state_list[i]["board"])
    #             if hash_board not in self.chess_dict:
    #                 self.chess_dict[hash_board] = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (1, 0): 0, (1, 1): 0, (1, 2): 0,
    #                                                (2, 0): 0, (2, 1): 0, (2, 2): 0}

    #             # 判断是否形成 “二连”
    #             is_good_operate = is_two_in_a_row(self.state_list[i]["board"], self.state_list[i]["operate"], self.chess)
    #             if is_good_operate:
    #                 self.chess_dict[hash_board][self.state_list[i]["operate"]] += 0.2 * self.value_rate

    #             # 判断是否形成“三连”
    #             is_good_operate_three = is_three_in_a_row(self.state_list[i]["board"], self.state_list[i]["operate"], self.chess)
    #             if is_good_operate_three:
    #                 self.chess_dict[hash_board][self.state_list[i]["operate"]] += 1 * self.value_rate

    #             # 判断是否有能直接赢的步没有下，没下则扣分
    #             position = find_win_move(self.state_list[i]["board"], self.chess)
    #             if position is not None and self.state_list[i]["operate"] != position:
    #                 self.chess_dict[hash_board][self.state_list[i]["operate"]] -= 2 * self.value_rate
    #                 self.chess_dict[hash_board][position] += 1.5 * self.value_rate
    #             else:
    #                 # 如果对面下一步能赢，没有堵住对面，也扣分
    #                 position_other = find_win_move(self.state_list[i]["board"], the_other_chess)
    #                 if position_other is not None and self.state_list[i]["operate"] != position_other:
    #                     self.chess_dict[hash_board][self.state_list[i]["operate"]] -= 2 * self.value_rate
    #                     self.chess_dict[hash_board][position_other] += 1.5 * self.value_rate

    #             # 胜利则奖励所有状态行动
    #             if is_win:
    #                 self.chess_dict[hash_board][self.state_list[i]["operate"]] += 1 * self.value_rate * (0.4 ** (len(self.state_list) - step))
        
    # 计算学习棋局行动价值
    def count_state_list(self, is_win, the_other_chess):
        if self.value_rate != 0:
            last_operate = board_to_hash(self.state_list[len(self.state_list)-1]["board"])
            if last_operate not in self.chess_dict:
                value = 0.5
                if is_win is True:
                    value = 1.0
                elif is_win is False:
                    value = 0
                self.chess_dict[last_operate] = value

            for i in range(len(self.state_list)-2, -1, -1):
                current_board = self.state_list[i]["board"]
                board_hash = board_to_hash(current_board)
                if board_hash not in self.chess_dict:
                    self.chess_dict[board_hash] = 0.5
                
                reward = 0
                
                self.chess_dict[board_hash] = self.chess_dict[board_hash] + self.epsilon*(reward + self.chess_dict[board_to_hash(self.state_list[i+1]["board"])] - self.chess_dict[board_hash])

    def reset_state_list(self):
        self.state_list = []

    def get_chess_dict(self):
        return self.chess_dict

    # 对局中根据学习到的数据，做出下棋决策
    def make_game_move(self, current_board, table_hash):
        copy_board = copy.deepcopy(current_board)
        # 获取空位置
        empty_indices = []
        for i in range(len(copy_board)):
            for j in range(len(copy_board[i])):
                if copy_board[i][j] == " ":
                    empty_indices.append((i, j))

        if self.epsilon <= random.random():
            value_arr = []
            for i in range(len(empty_indices)):
                copy_board[empty_indices[i][0]][empty_indices[i][1]] = self.chess
                step_hash = board_to_hash(copy_board)
                if step_hash in self.chess_dict:
                    value_arr.append(self.chess_dict[step_hash])
                else:
                    value_arr.append(0)
                copy_board[empty_indices[i][0]][empty_indices[i][1]] = " "
        
            max_value = max(value_arr)  # 获取数组中的最大值
            max_indices = [i for i, value in enumerate(value_arr) if value == max_value] 
            choice = random.choice(max_indices)
            copy_board[empty_indices[choice][0]][empty_indices[choice][1]] = self.chess
            self.state_list.append({"board": copy_board, "operate": empty_indices[choice]})
            return empty_indices[choice]

        # 随机取一个
        random_index = random.choice(empty_indices)
        copy_board[random_index[0]][random_index[1]] = self.chess
        self.state_list.append({"board": copy_board, "operate": random_index})
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