import RL

if __name__ == "__main__":

    round_times = 1   # 训练轮次
    one_round_time = 20     # 每轮进行多少次对局
    debug_mode = True

    for i in range(round_times):
        print("第"+str(i)+"轮训练开始-------------------")
        RL.Rl(one_round_time, debug_mode)