import random
import gym
from gym import spaces
import numpy as np
from position.calculate_reward import calculate_position_reward


DAYS_PER_STEP = 7
TIMESTEPS = 150000
INITIAL_ACCOUNT_BALANCE = 0


class PositionCuratorEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(PositionCuratorEnv, self).__init__()

        self.df = df
        self.actions = []
        self.current_day = 0
        self.current_step = 0
        self.total_steps = 0
        self.days_left = DAYS_PER_STEP

        # Actions of the format 0 - do nothing, 1 - build a path, 2 - build evac path
        self.action_space = spaces.Discrete(3)

        # Space contains the last five events
        self.observation_space = spaces.Box(low=0, high=23, shape=(4,), dtype=np.float16)

    def _next_observation(self):
        get_curr_position = self.current_day * 96 + self.current_step

        # Get the last event
        frame = self.df.iloc[get_curr_position].to_numpy()

        return frame

    def _take_action(self, action):
        self.actions.append(action)

    def step(self, action):
        # Execute one time step within the environment
        self._take_action(action)

        reward = calculate_position_reward(df=self.df.iloc[self.current_day * 96 + self.current_step], action=action)

        self.current_step += 1
        self.total_steps += 1

        done = False

        if self.current_step == 96:
            # get_curr_position = self.current_day * 96
            # reward = calculate_position_reward(df=self.df.loc[get_curr_position: get_curr_position + 95], actions=self.actions)

            self.actions = []
            self.current_day += 1
            self.current_step = 0
            self.days_left -= 1

        reward = reward * (self.total_steps / TIMESTEPS)

        obs = self._next_observation()

        if self.days_left == 0:
            done = True

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.actions = []
        self.current_step = 0
        self.days_left = DAYS_PER_STEP

        # Set the current day to a random point within the data frame
        number_of_rows = int(len(self.df.index) / 96)
        self.current_day = random.randint(0, number_of_rows - DAYS_PER_STEP - 1)

        return self._next_observation()

    def render(self, mode='human', close=False):
        print(f'Step: {self.current_step}')
