import numpy as np
from stable_baselines3 import PPO, A2C, DQN
import random
import pandas as pd
import matplotlib.pyplot as plt

model = DQN.load('position_model')


def random_position_event(hour_from=0, hour_to=23, build_path=0, evacuation=0):
    return [[random.randint(hour_from, hour_to) / 24, random.randint(0, 3) / 4, build_path, evacuation]]


build_path = []
build_evac_path = []
build_path_night = []
build_evac_path_night = []

for k in range(1000):
    action, _states = model.predict(np.array(random_position_event(8, 20, 1)))
    build_path.append(action[0])

print(f'Точность для построения пути днём: {round(build_path.count(1) / len(build_path), 2) * 100}%')

for k in range(1000):
    action, _states = model.predict(np.array(random_position_event(8, 20, 0, 1)))
    build_evac_path.append(action[0])

print(f'Точность для построения пути для эвакуации днём: {round(build_evac_path.count(2) / len(build_evac_path), 2) * 100}%')

for k in range(1000):
    action, _states = model.predict(np.array(random_position_event(0, 7, 1)))
    build_path_night.append(action[0])

print(f'Точность для построения пути ночью: {round(build_path_night.count(0) / len(build_path_night), 2) * 100}%')

for k in range(1000):
    action, _states = model.predict(np.array(random_position_event(0, 7, 0, 1)))
    build_evac_path_night.append(action[0])


print(f'Точность для построения пути для эвакуации ночью: {round(build_evac_path_night.count(0) / len(build_evac_path_night), 2) * 100}%')

logs = pd.read_csv('./log/monitor.csv', skiprows=1)

plt.clf()
plt.plot(logs['r'], color='darkorange')
plt.xlabel('Iteration')
plt.ylabel('Reward')
plt.title('Position: Rewards over time')
plt.show()
