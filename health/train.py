from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.utils import get_linear_fn
import pandas as pd

from health.env import HealthCuratorEnv, TIMESTEPS

df = pd.read_csv('../data.csv')

df = df.drop(['strangerArrived', 'illWorkerArrived', 'buildPath', 'emergencyStart'], axis=1)

df['hour'] = df['hour'] / 24
df['minute'] = df['minute'] / 4

env = Monitor(HealthCuratorEnv(df), filename='log')

checkpoint_callback = CheckpointCallback(save_freq=int(TIMESTEPS / 10), save_path='./log/checkpoints/', name_prefix='health_checkpoint')

# model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./log/")
model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./log/", exploration_fraction=0.3)

model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)

model.save("health_model")
