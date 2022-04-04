import time

import numpy as np
import pandas as pd


def load_grid(filename):
    grid = pd.read_csv(filename, '\t', header=None).to_numpy()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                s = (i, j)
            if grid[i][j] == "X":
                x = (i, j)

    return grid, s, x


class State:
    def __init__(self, board, barrier, state):
        self.board = board
        self.state = state
        self.barrier = barrier

    def give_reward(self, board, reward):
        i, j = self.state
        if board[i][j] in range(-9, 9) and board[i][j] != 0:
            return board[i][j]
        else:
            return reward

    def next_position(self, action):
        if action == "up":
            nxtState = (self.state[0] - 1, self.state[1])
        elif action == "down":
            nxtState = (self.state[0] + 1, self.state[1])
        elif action == "left":
            nxtState = (self.state[0], self.state[1] - 1)
        else:
            nxtState = (self.state[0], self.state[1] + 1)

        # check if position is good
        if (nxtState[0] >= 0) and (nxtState[0] < len(self.board)):
            if (nxtState[1] >= 0) and (nxtState[1] < len(self.board[0])):
                if nxtState != self.barrier:
                    return nxtState
        return self.state

    def prob_action(self, action):
        if action == "up":
            return np.random.choice(["up", "left", "right"], p=[0.8, 0.1, 0.1])
        if action == "down":
            return np.random.choice(["down", "left", "right"], p=[0.8, 0.1, 0.1])
        if action == "left":
            return np.random.choice(["left", "up", "down"], p=[0.8, 0.1, 0.1])
        if action == "right":
            return np.random.choice(["right", "up", "down"], p=[0.8, 0.1, 0.1])

    def show_board(self):
        self.board[self.state] = 1
        for i in range(0, len(self.board)):
            print('-----------------')
            out = '| '
            for j in range(0, len(self.board[0])):
                if self.board[i, j] == 'X':
                    token = 'X'
                if self.board[i, j] == 'S':
                    token = 'S'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
            print(out)
        print('-----------------')


class Agent:

    def __init__(self, file, reward_per_action, gamma, time_to_learn, prob_of_moving):
        self.grid, self.start, self.barrier = load_grid(file)
        self.gamma = gamma
        self.states = []
        self.reward = reward_per_action
        self.learn_time = time_to_learn
        self.prob = prob_of_moving
        # t0 = time.time()
        self.state = self.start
        self.State = State(self.grid, self.barrier, self.start)
        self.actions = ["up", "down", "left", "right"]
        self.lr = 0.2

        # initial Q values
        self.Q_values = {}
        board_rows = len(self.grid)
        board_cols = len(self.grid[0])

        for i in range(board_rows):
            for j in range(board_cols):
                self.Q_values[(i, j)] = {}
                for a in self.actions:
                    self.Q_values[(i, j)][a] = 0  # Q value is a dict of dict

    def choose_action(self):
        # choose action with most expected value
        mx_nxt_reward = 0
        action = ""

        if np.random.uniform(0, 1) <= self.gamma:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                current_position = self.State.state
                nxt_reward = self.Q_values[current_position][a]
                if nxt_reward >= mx_nxt_reward:
                    action = a
                    mx_nxt_reward = nxt_reward
            # print("current pos: {}, greedy aciton: {}".format(self.State.state, action))
        return action

    def determine_action(self):
        # choose action with most expected value
        mx_nxt_reward = 0
        action = ""

        if np.random.uniform(0, 1) <= self.gamma:
            action = np.random.choice(self.actions)
        else:
            # greedy action
            for a in self.actions:
                current_position = self.State.state
                nxt_reward = self.Q_values[current_position][a]
                if nxt_reward >= mx_nxt_reward:
                    action = a
                    mx_nxt_reward = nxt_reward
            # print("current pos: {}, greedy aciton: {}".format(self.State.state, action))
        return action

    def takeAction(self, action):
        position = self.State.next_position(action)
        # update State
        return State(self.grid, self.barrier, position)

    def reset(self):
        self.states = []
        self.State = State(self.grid, self.barrier, self.start)

    def play(self, t0):
        timeout = time.time() + t0
        while True:
            if time.time() <= timeout:
                # to the end of game back propagate reward
                action = self.choose_action()
                # append trace
                self.states.append([(self.State.state), action])
                print("current position {} action {}".format(self.State.state, action))
                # by taking the action, it reaches the next state
                self.State = self.takeAction(action)
                # # mark is end
                # self.State.isEndFunc()
                # print("nxt state", self.State.state)
                # print("---------------------")
                # self.isEnd = self.State.isEnd
            else:
                # back propagate
                reward = self.State.give_reward(self.grid, self.reward)
                for a in self.actions:
                    self.Q_values[self.State.state][a] = reward
                print("Game End Reward", reward)
                for s in reversed(self.states):
                    current_q_value = self.Q_values[s[0]][s[1]]
                    reward = current_q_value + self.lr * (self.gamma * reward - current_q_value)
                    self.Q_values[s[0]][s[1]] = round(reward, 3)

                self.reset()
                break


if __name__ == "__main__":
    ag = Agent('grid_sample.txt', 1, 0.3, 30, 0.8)
    print("initial Q-values ... \n")
    print(ag.Q_values)

    ag.play(5)
    print("latest Q-values ... \n")
    print(ag.Q_values)
