import random
import numpy as np
import pickle

class ComputerPlayer:
    def __init__(self, name, hash, exp_rate = 0.8 ):
        self.states = []
        self.name = name
        self.hash = hash
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.q_value = {}
    
    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) < self.exp_rate:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            allposval = []

            random.shuffle(positions)
            # print(positions)
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.hash.getSymmetryHash(next_board)
                self.hash.reset()
                value = 0 if self.q_value.get(next_boardHash) is None else self.q_value.get(next_boardHash)
                allposval.append(value)
                if value > value_max:
                    value_max = value
                    action = p
            # print(allposval)
        return action

    def addState(self, state):
        self.states.append(state)

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.q_value.get(st) is None:
                self.q_value[st] = 0
            self.q_value[st] += self.lr * (self.decay_gamma * reward - self.q_value[st])
            reward = self.q_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        with open('model_.'+str(self.name), 'wb') as fw:
            pickle.dump(self.q_value, fw)

    def loadPolicy(self, file):
        with open(file, 'rb') as fr:
            self.q_value = pickle.load(fr)

    def saveTrainedModel(self, q1, q2):
        q_value = {}
        for key, val in q1.items():
            q_value[key] = val
        for key, val in q2.items():
            q_value[key] = val
        with open('h5_.'+str(self.name), 'wb') as fw:
            pickle.dump(q_value, fw)

class HumanPlayer:
    def __init__(self, name):
        self.name = name
    
    def chooseAction(self, positions, current_board=[], symbol=1):
        while True:
            row = int(input("Input your action row:"))
            col = int(input("Input your action col:"))
            action = (row, col)
            if action in positions:
                return action
            else:
                print("Illegal move !?!")
            
    def addState(self, state):
        pass

    def feedReward(self, reward):
        pass

    def reset(self):
        pass