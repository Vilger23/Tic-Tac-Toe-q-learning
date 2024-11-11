from src.AI import AI
from src.gui import GUI
from src.game import Game
import os

def main():
	#os.system('.\src\install_dependicies.bat')
	scale = 0.9

	ai = AI(training=False)
	game = Game(ai)
	GUI(game, scale)

if __name__ == '__main__':
	main()