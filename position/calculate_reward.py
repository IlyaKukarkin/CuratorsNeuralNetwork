def calculate_position_reward(df, action):
    hour = df['hour'] * 24
    build_path = df['buildPath']
    emergency = df['emergencyStart']

    if 8 <= hour < 20:
        if build_path and action == 1:
            return 100

        if build_path and action != 1:
            return -100

        if emergency and action == 2:
            return 100

        if emergency and action != 2:
            return -100
    else:
        if (build_path or emergency) and action != 0:
            return -100
        else:
            return 50

    return 0

def calculate_position_reward_day(df, actions):
    res = 0
    number_of_workers = 0

    hour = df['hour'].values
    worker_arrived = df['workerArrived'].values
    stranger_arrived = df['strangerArrived'].values
    ill_worker_arrived = df['illWorkerArrived'].values

    for index, value in enumerate(actions):
        if 8 <= hour[index] < 20:
            if worker_arrived[index] and value:
                number_of_workers += 1

            if stranger_arrived[index] and value:
                res -= 50

            if ill_worker_arrived[index] and value:
                res -= 50

            if value:
                res -= 1
            else:
                res += 5

            if (index + 1) % 4 == 0:
                res += number_of_workers * 1000
        else:
            if value:
                res -= 1
            else:
                res += 5

    return res
