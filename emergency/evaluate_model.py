import numpy as np
from stable_baselines3 import PPO, A2C, DQN
import random
import pandas as pd
import matplotlib.pyplot as plt

model = DQN.load('emergency_model')


def random_emergency_event(hour_from=0, hour_to=23, emergency_start=0):
    return [[random.randint(hour_from, hour_to) / 24, random.randint(0, 3) / 4, emergency_start]]


emergency_start = []
emergency_start_night = []

for k in range(1000):
    action, _states = model.predict(np.array(random_emergency_event(8, 20, 1)))
    emergency_start.append(action[0])

print(f'Точность для вызова полиции днём: {round(np.mean(emergency_start), 1) * 100}%')

for k in range(1000):
    action, _states = model.predict(np.array(random_emergency_event(0, 7, 0)))
    emergency_start_night.append(action[0])

print(f'Точность для вызова полиции ночью: {round(1 - np.mean(emergency_start_night), 1) * 100}%')

logs = pd.read_csv('./log/monitor.csv', skiprows=1)

plt.clf()
plt.plot(logs['r'], color='darkorange')
plt.xlabel('Iteration')
plt.ylabel('Reward')
plt.title('Emergency: Rewards over time')
plt.show()
