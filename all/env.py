import random
import gym
from gym import spaces
import numpy as np
from all.calculate_reward import calculate_all_reward


DAYS_PER_STEP = 7
INITIAL_ACCOUNT_BALANCE = 0
TIMESTEPS = 250000


class AllCuratorEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(AllCuratorEnv, self).__init__()

        self.df = df
        self.actions = []
        self.current_day = 0
        self.current_step = 0
        self.total_steps = 0
        self.days_left = DAYS_PER_STEP
        self.balance = INITIAL_ACCOUNT_BALANCE

        # Actions of the format 0 - do nothing, 1 - allow to enter and so on
        self.action_space = spaces.Discrete(5)

        # Space contains the last five events
        self.observation_space = spaces.Box(low=0, high=1, shape=(2, 9), dtype=np.uint8)

    def _next_observation(self):
        get_curr_position = self.current_day * 96 + self.current_step

        # Get the last two events
        frame = self.df.iloc[get_curr_position: get_curr_position + 2].to_numpy()

        return frame

    def _take_action(self, action):
        self.actions.append(action)

    def step(self, action):
        # Execute one time step within the environment
        self._take_action(action)

        self.current_step += 1
        self.total_steps += 1

        reward = calculate_all_reward(df=self.df.loc[self.current_day + self.current_step: self.current_day + self.current_step + 1], action=action)

        done = False

        if self.current_step == 96:
            # get_curr_position = self.current_day * 96
            # reward = calculate_all_reward(df=self.df.loc[get_curr_position: get_curr_position + 95], actions=self.actions)

            self.actions = []
            self.current_day += 1
            self.current_step = 0
            self.days_left -= 1

        obs = self._next_observation()

        reward = reward * (self.total_steps / TIMESTEPS)

        if self.days_left == 0:
            done = True

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.actions = []
        self.current_step = 0
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.days_left = DAYS_PER_STEP

        # Set the current day to a random point within the data frame
        number_of_rows = int(len(self.df.index) / 96)
        self.current_day = random.randint(0, number_of_rows - DAYS_PER_STEP)

        return self._next_observation()

    def render(self, mode='human', close=False):
        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
