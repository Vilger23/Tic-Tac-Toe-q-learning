from src.AI import *
import pickle

class Game():
    def __init__(self, ai):
        self.ai = ai
        self.ai.game = self
        self.board = 9*(0,)
        self.time_line = list()
        self.current_player = 1
        self.ai_starting = False
        if self.ai.training:
            self.ai.training_loop()
        self.num_to_char = {
            -1: 'O',
            0:  ' ',
            1:  'X'
        }


    def check_for_win(self, state):
        # start, steps, stop
        lines = [
            (0,1,2), (3,4,5), (6,7,8), 
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
            ]

        for line in lines:
            char = set()
            for index in line:
                char.add(state[index])
            if len(char) == 1 and state[line[0]] != 0:
                return state[line[0]]
        return 0

    def update_board(self, action):
        self.current_player *= -1
        self.time_line.append( (self.board, action) )
        self.board = tuple((i + j for i, j in zip(self.board, action)))



    def action(self, a):
        self.update_board(a)
        if self.check_for_win(self.board) == self.current_player*-1:
            print('You won!')
            self.time_line = self.time_line[:-1]
            self.ai.update_q_values(-1)
            self.reset()
        elif not self.ai.get_possible_actions(self.board):
            print('Draw!')
            self.reset()
        else:
            self.ai_play()

    def reset(self):
        self.board = (0,)*9
        self.current_player = 1
        self.time_line = list()
        if self.ai_starting:
            self.ai_play()

    def ai_play(self):
        action = self.ai.choose_action(self.board, training = False)
        self.update_board(action)
        
        if self.check_for_win(self.board) == self.current_player*-1:
            print('ai won!')
            self.reset()
        elif not self.ai.get_possible_actions(self.board):
            print('Draw!')
            self.reset()