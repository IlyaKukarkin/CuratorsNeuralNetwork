def calculate_health_reward(df, action):
    hour = df['hour'].values * 24
    worker_fell = df['workerFell'].values
    worker_stand_up = df['workerStandUp'].values

    if 8 <= hour[1] < 20:
        if worker_fell[0] and not action and not worker_stand_up[1]:
            return -1000

        if worker_fell[0] and action and not worker_stand_up[1]:
            return 2000

        if worker_fell[0] and not action and worker_stand_up[1]:
            return 2000
    else:
        if action:
            return -100
        else:
            return 2

    return 0

def calculate_health_reward_day(df, actions):
    res = 0
    number_of_workers = 0

    fallen_index = 0

    hour = df['hour'].values * 24
    worker_arrived = df['workerArrived'].values
    worker_fell = df['workerFell'].values
    worker_stand_up = df['workerStandUp'].values

    for index, value in enumerate(actions):
        if 8 <= hour[index] < 20:
            if worker_arrived[index]:
                number_of_workers += 1

            if worker_fell[index]:
                fallen_index = index

            if fallen_index == index - 1 and not value and not worker_stand_up[index]:
                fallen_index = 0
                number_of_workers -= 1

            # if value:
            #     res -= 10000
            # else:
            #     res += 500

            if (index + 1) % 4 == 0:
                res += abs(number_of_workers) * 1000
        else:
            if value:
                res -= 100
            else:
                res += 2

    return res
