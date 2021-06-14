from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.utils import get_linear_fn
import pandas as pd

from position.env import PositionCuratorEnv, TIMESTEPS

df = pd.read_csv('../data.csv')

df = df.drop(['workerFell', 'workerStandUp', 'workerArrived', 'illWorkerArrived', 'strangerArrived'], axis=1)

df['hour'] = df['hour'] / 24
df['minute'] = df['minute'] / 4

env = Monitor(PositionCuratorEnv(df), filename='log')

checkpoint_callback = CheckpointCallback(save_freq=int(TIMESTEPS / 10), save_path='./log/checkpoints/', name_prefix='position_checkpoint')

model = DQN('MlpPolicy', env, verbose=1, tensorboard_log="./log/", exploration_fraction=0.4)
# model = DQN('MlpPolicy', env, verbose=1, tensorboard_log="./log/")

model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)

model.save("position_model")
