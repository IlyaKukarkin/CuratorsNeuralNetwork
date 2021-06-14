import numpy as np
from stable_baselines3 import PPO, A2C, DQN
import random
import pandas as pd
import matplotlib.pyplot as plt

model = DQN.load('health_model')


def random_health_event(worker_fell=0, worker_stand_up=0):
    hour = random.randint(8, 20)
    minute = random.randint(0, 3)

    if minute == 3:
        return [[hour / 24, minute / 4, 0, worker_fell, 0],
                [(hour + 1) / 24, 0, 0, 0, worker_stand_up]]

    return [[hour / 24, minute / 4, 0, worker_fell, 0],
            [hour / 24, (minute + 1) / 4, 0, 0, worker_stand_up]]


worker_saved = []
worker_stand_up = []

for k in range(1000):
    action, _states = model.predict(np.array(random_health_event(1, 0)))
    worker_saved.append(action)

print(f'Точность для упавшего сотрудника: {round(np.mean(worker_saved), 1) * 100}')

for k in range(1000):
    action, _states = model.predict(np.array(random_health_event(1, 1)))
    worker_stand_up.append(action)

print(f'Точность для упавшего и вставшего на ноги человека: {round(1 - np.mean(worker_stand_up), 1) * 100}')

logs = pd.read_csv('./log/monitor.csv', skiprows=1)

plt.clf()
plt.plot(logs['r'], color='darkorange')
plt.xlabel('Iteration')
plt.ylabel('Reward')
plt.title('Health: Rewards over time')
plt.show()
