import RL

if __name__ == "__main__":

    round_times = 100   # 训练轮次
    one_round_time = 10000     # 每轮进行多少次对局

    for i in range(round_times):
        RL.Rl(one_round_time)
