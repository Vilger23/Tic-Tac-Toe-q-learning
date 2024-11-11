from src.AI import *
from src.game import *
import argparse
import os

def train(kwargs):
	ai = AI(training = True, **kwargs)
	game = Game(ai)
	ans = input('Initialize game-loop (y/n)?')
	if ans == 'y':
		os.system('python main_app.py')

if __name__ == '__main__':

	os.system('')
	parser = argparse.ArgumentParser()

	parser.add_argument('--epochs', type=int, required=False)
	parser.add_argument('--epsilon', type=int, required=False)
	parser.add_argument('--gamma', type=int, required=False)
	parser.add_argument('--alpha', type=int, required=False)

	args = parser.parse_args()

	kwargs = dict()
	kwargs['epochs'] = args.epochs
	kwargs['epsilon'] = args.epsilon
	kwargs['gamma'] = args.gamma
	kwargs['alpha'] = args.alpha
	kwargs = {k: v for k, v in kwargs.items() if v}

	train(kwargs)
