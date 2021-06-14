def calculate_emergency_reward(df, action):
    hour = df['hour'] * 24
    emergency_start = df['emergencyStart']

    if 8 <= hour < 20:
        if emergency_start and action:
            return 300

        if emergency_start and not action:
            return -100

        if not emergency_start and action:
            return -100

        if not emergency_start and not action:
            return 100
    else:
        if action:
            return -30

    return 0


def calculate_emergency_reward_day(df, actions):
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
