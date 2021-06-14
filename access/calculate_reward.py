def calculate_access_reward(df, action):
    hour = df['hour'] * 24
    worker_arrived = df['workerArrived']
    stranger_arrived = df['strangerArrived']
    ill_worker_arrived = df['illWorkerArrived']

    if 8 <= hour < 20:
        if worker_arrived and action:
            return 500

        if stranger_arrived and action:
            return -1000

        if ill_worker_arrived and action:
            return -1000
    else:
        if worker_arrived and action:
            return -1000

    # if not action:
    #     return 10

    return 0


def calculate_access_reward_day(df, actions):
    res = 0
    number_of_workers = 0

    hour = df['hour'].values * 24
    worker_arrived = df['workerArrived'].values
    stranger_arrived = df['strangerArrived'].values
    ill_worker_arrived = df['illWorkerArrived'].values

    for index, value in enumerate(actions):
        if 8 <= hour[index] < 20:
            if worker_arrived[index] and value:
                number_of_workers += 1

            if stranger_arrived[index] and value:
                res -= 10000

            if ill_worker_arrived[index] and value:
                res -= 10000

            # if value:
            #     res += 1000
            # else:
            #     res -= 1000

            if (index + 1) % 4 == 0:
                res += number_of_workers * 1000
        # else:
        #     if value:
        #         res += 1000
        #     else:
        #         res -= 1000

    return res
