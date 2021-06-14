from stable_baselines3 import PPO, A2C, DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
import pandas as pd

from all.env import AllCuratorEnv, TIMESTEPS

df = pd.read_csv('../data.csv')

df['hour'] = df['hour'] / 24
df['minute'] = df['minute'] / 4

env = Monitor(AllCuratorEnv(df), filename='log')

checkpoint_callback = CheckpointCallback(save_freq=int(TIMESTEPS / 10), save_path='./log/checkpoints/', name_prefix='all_checkpoint')

# model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./log/", learning_rate=3e-1)
# model = A2C("MlpPolicy", env, verbose=1, tensorboard_log="./log/")
model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./log/", exploration_fraction=0.4)

model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)

model.save("all_model")
