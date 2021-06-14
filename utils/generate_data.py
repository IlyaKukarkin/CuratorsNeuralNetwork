import os
import random
import pandas
from collections import deque
from datetime import datetime


def delete_temp_file():
    try:
        os.remove('temp.csv')
    except OSError:
        print("Deletion of the temp.csv failed")
    else:
        print("Successfully deleted the temp.csv")


def delete_data_file():
    try:
        os.remove('./data.csv')
    except OSError:
        print("Deletion of the data.csv failed")
    else:
        print("Successfully deleted the data.csv")


def create_df_columns(columns):
    res = ['hour', 'minute']

    for ev in columns:
        res.append(ev)

    return res


def print_percent(percent):
    print("\r", end="")
    print(f'{int(percent * 100)}%', end="")


if __name__ == '__main__':
    n = 100000
    k = 1000

    percent = 0
    percent_increase = k / n

    print(datetime.now())

    input_events = {
        'access': ['workerArrived', 'strangerArrived', 'illWorkerArrived'],
        'health': ['workerFell', 'workerStandUp'],
        'position': ['buildPath', 'buildEvacPath'],
        'emergency': ['emergencyStart']
    }

    delete_data_file()
    delete_temp_file()

    n_base = 100 * n
    n_custom = n_base * 3

    print('Generating random sequences...')

    print_percent(0.2)
    random_arrived = deque(random.choices(population=[0, 1], weights=[0.3, 0.7], k=n_base))
    random_arrived_night = deque(random.choices(population=[0, 1], weights=[0.8, 0.2], k=n_base))

    print_percent(0.3)
    random_arrived_type = deque(
        random.choices(population=['workerArrived', 'illWorkerArrived', 'strangerArrived'], weights=[0.8, 0.1, 0.1], k=n_base))

    print_percent(0.4)
    random_arrived_stranger = deque(random.choices(population=[0, 1], weights=[0.97, 0.03], k=n_base))

    print_percent(0.5)
    random_fall = deque(random.choices(population=[0, 1], weights=[0.75, 0.25], k=n_base))

    print_percent(0.6)
    random_stand_up = deque(random.choices(population=[0, 1], weights=[0.3, 0.7], k=n_base))

    print_percent(0.7)
    random_path = deque(random.choices(population=[0, 1], weights=[0.7, 0.3], k=n_base))

    print_percent(0.8)
    random_path_evac = deque(random.choices(population=[0, 1], weights=[0.3, 0.7], k=n_base))

    print_percent(0.9)
    random_emergency = deque(random.choices(population=[0, 1], weights=[0.9, 0.1], k=n_base))

    print("\r", end="")
    print('100%')

    print('Starting generation...')

    while n > 0:
        print_percent(percent)
        p = k

        events_list = []

        events_df = pandas.DataFrame()

        while p > 0:
            for hour in range(24):
                isFall = False

                for minute in range(4):

                    temp_dict = {
                        'hour': hour,
                        'minute': minute,
                        'workerArrived': 0,
                        'illWorkerArrived': 0,
                        'strangerArrived': 0,
                        'workerFell': 0,
                        'workerStandUp': 0,
                        'buildPath': 0,
                        'emergencyStart': 0,
                    }

                    # Эвакуация
                    emergency_start = random_emergency.popleft()

                    if emergency_start:
                        temp_dict['emergencyStart'] = emergency_start
                        events_list.append(temp_dict)
                        continue

                    # Построить путь
                    build_path = random_path.popleft()

                    if build_path:
                        temp_dict['buildPath'] = build_path
                        events_list.append(temp_dict)
                        continue

                    # Упал сотрудник
                    worker_fell = random_fall.popleft()
                    worker_stand_up = random_stand_up.popleft()

                    if isFall:
                        temp_dict['workerStandUp'] = worker_stand_up
                        isFall = False
                        events_list.append(temp_dict)
                        continue

                    if worker_fell:
                        temp_dict['workerFell'] = worker_fell
                        isFall = True
                        events_list.append(temp_dict)
                        continue

                    # Кто-то пришёл (сотрудник, чужой человек, больной сотрудник)
                    if 8 <= hour < 20:
                        temp_dict[random_arrived_type.popleft()] = random_arrived.popleft()
                    else:
                        temp_dict[random_arrived_type.popleft()] = random_arrived_night.popleft()

                    events_list.append(temp_dict)

            p -= 1

        events_df = events_df.append(events_list, ignore_index=True)

        if percent == 0:
            events_df.to_csv("temp.csv", sep=',', index=False)
        else:
            events_df.to_csv("temp.csv", mode='a', header=False, sep=',', index=False)

        percent += percent_increase
        n -= k

    print("\r", end="")
    print('100%')

    print('Reading temp files...')
    df_final = pandas.read_csv("temp.csv")

    print('Removing Null values...')
    df_final = df_final.fillna(0)

    print('Changing all values to int...')
    df_final = df_final.astype(int)

    print('Creating final files...')
    df_final.to_csv("./data.csv", sep=',', index=False)

    delete_temp_file()

    print(datetime.now())
