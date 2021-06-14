import numpy as np
from stable_baselines3 import PPO, DQN
import random
import pandas as pd
import matplotlib.pyplot as plt

model = DQN.load('all_model')


def random_all_event(hour_from=0, hour_to=23, worker_arrived=0, strander_arrived=0, ill_worker_arrived=0):
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [random.randint(hour_from, hour_to) / 24, random.randint(0, 3) / 4, worker_arrived, strander_arrived,
             ill_worker_arrived, 0, 0, 0, 0]]


worker_arrived = []
stranger_arrived = []
ill_worker_arrived = []

for k in range(1000):
    action, _states = model.predict(np.array(random_all_event(8, 20, 1)))
    worker_arrived.append(action)

print(f'Точность для прибывшего днём сотрудника: {round(np.mean(worker_arrived), 1) * 100}%')

for k in range(1000):
    action, _states = model.predict(np.array(random_all_event(0, 23, 0, 1)))
    print(action)
    worker_arrived.append(action)

print(f'Точность для прибывшего чужого человека: {round(1 - np.mean(worker_arrived), 1) * 100}%')

for k in range(1000):
    action, _states = model.predict(np.array(random_all_event(0, 23, 0, 0, 1)))
    worker_arrived.append(action)

print(f'Точность для прибывшего больного сотрудника: {round(1 - np.mean(worker_arrived), 1) * 100}%')

for k in range(1000):
    action, _states = model.predict(np.array(random_all_event(0, 7, 1)))
    worker_arrived.append(action)

print(f'Точность для прибывшего ночью сотрудника: {round(1 - np.mean(worker_arrived), 1) * 100}%')

logs = pd.read_csv('./log/monitor.csv', skiprows=1)

plt.clf()
plt.plot(logs['r'], color='darkorange')
plt.xlabel('Iteration')
plt.ylabel('Reward')
plt.title('All: Rewards over time')
plt.show()
