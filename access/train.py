from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.utils import get_linear_fn
import pandas as pd

from access.env import AccessCuratorEnv, TIMESTEPS

df = pd.read_csv('../data.csv')

df = df.drop(['workerFell', 'workerStandUp', 'buildPath', 'emergencyStart'], axis=1)

df['hour'] = df['hour'] / 24
df['minute'] = df['minute'] / 4

env = Monitor(AccessCuratorEnv(df), filename='log')

checkpoint_callback = CheckpointCallback(save_freq=int(TIMESTEPS / 10), save_path='./log/checkpoints/', name_prefix='access_checkpoint')

# model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./log/")
# model = A2C("MlpPolicy", env, verbose=1, tensorboard_log="./log/", learning_rate=get_linear_fn(1e-6, 1e-1, 0.85))
# model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./log/", exploration_fraction=0.3, learning_rate=get_linear_fn(1e-6, 1e-1, 1))
model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./log/", exploration_fraction=0.4)
# model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./log/")

model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)

model.save("access_model")
