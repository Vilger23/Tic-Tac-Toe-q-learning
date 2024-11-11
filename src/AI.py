import time
import random
import pickle
import glob
import os
import sys

def timer(func):
    def wrapper(*args, **kwargs):
        print(f'{func.__name__} function called')

        AI.start = time.time()
        func(*args, **kwargs)
        end = time.time()
        elapsed_time = end-AI.start

        print(f'{func.__name__} function finished in {round(elapsed_time, 2)}s')

    return wrapper

class bcolors:
    OKGREEN = '\033[92m'
    BACKGROUND = '\033[47m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

class AI:
    def __init__(self, training = False, alpha = 0.15, epsilon = 0.35, gamma = 0.9, epochs = 100_000):
        self.game = None
        self.training = training
        if training is False:
            self.q = self.load_saved_model()
        else:
            self.q = dict()

        self.alpha = alpha
        self.epsilon = epsilon
        self.epochs = epochs
        self.gamma = gamma

    def load_saved_model(self):
        list_of_files = glob.glob('./src/saved_models/*.pickle')
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'rb') as file:
            pre_trained_model = pickle.load(file)
        self.current_model = latest_file
        return pre_trained_model
        
    def get_q_value(self, state, action):
        try:
            return self.q[tuple(state)][tuple(action)]
        except KeyError:
            return 0

    def update_q_values(self, reward):
        time_line = self.game.time_line
        time_line.reverse()
        for iterator in time_line[::2]:
            s, a = iterator
            self.q.setdefault(s, dict())
            old_q = self.get_q_value(s, a)

            self.q[s][a] = old_q + self.alpha * (reward - old_q)
            reward *= self.gamma

    def state_after_action(self, state, action):
        new_state = tuple((i + j for i, j in zip(state, action)))
        return new_state

    def reverse(self, state):
        state = tuple(c*-1 for c in state)
        return state

    def get_possible_actions(self, state):
        possible_actions = list()
        action_template = [0,]*9
        for i, char in enumerate(state):
            if not char:
                new_action = action_template[:]
                new_action[i] = self.game.current_player
                possible_actions.append(tuple(new_action))
        return possible_actions

    def choose_action(self, state, training=True):
        possible_actions = self.get_possible_actions(state)

        explore = random.random() < self.epsilon and training

        if explore:
            action = random.choice(possible_actions)
        else:
            Q_vals = [ (self.get_q_value(state, a), a) for a in possible_actions]
            action = max(Q_vals, key = lambda x:x[0])
            action = action[1]

        if action is False:
            print(action, self.game.board)
        assert action is not False
        return action

    def display_training_progress(self, i):
        percent_done = (i+1)/self.epochs
        num_chars = 50
        colored = int(num_chars*percent_done)
        non_colored = num_chars - colored

        if i > 100:
            for _ in range(5):
                sys.stdout.write('\x1b[2K')
                sys.stdout.write('\x1b[1A')
        char = '-'
        loaded_char = ' '
        end = time.time()
        elapsed_time = end-AI.start

        print(f'Q-learning algorithm initialized\n\n{bcolors.BACKGROUND} {loaded_char*colored}{bcolors.ENDC} {char*non_colored}{round(percent_done*100, 2)}% done\n\ngames played: {i+1}/{self.epochs}\nestimated time left: {round( elapsed_time* (1/percent_done) - elapsed_time, 1)} seconds', end = '\r')

    @timer
    def training_loop(self):
        for i in range(self.epochs):
            if (i+1)%1000000 == 0:
                self.epsilon*=0.9
            if (i+1)%1000 == 0 or i == self.epochs - 1:
                self.display_training_progress(i) 
            while True:
                state = self.game.board
                action = self.choose_action(state)
                self.game.update_board(action)

                win = self.game.check_for_win(self.game.board)
                if win == self.game.current_player*-1:
                    self.update_q_values(1)
                    self.game.time_line = self.game.time_line[:-1]
                    self.update_q_values(-1)
                    break
                elif win == self.game.current_player:
                    self.update_q_values(-1)
                    self.game.time_line = self.game.time_line[:-1]
                    self.update_q_values(1)
                    break
                elif not self.get_possible_actions(self.game.board):
                    break
            self.game.reset() 

        model_dir = f'./src/saved_models/savedmodel%alpha={self.alpha}%epsilon={self.epsilon}%gamma={self.gamma}%epochs={self.epochs}%.pickle'
        with open(model_dir, 'wb') as file:
            pickle.dump(self.q, file, protocol = pickle.HIGHEST_PROTOCOL)
        self.current_model = model_dir
        print(self.q)
