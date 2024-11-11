from src.pages import gamepage, startpage, statspage, infopage
import pygame as pg
from pygame.locals import *
import sys

class GUI():
	def __init__(self, game, scale):
		self.scale = scale
		self.screensize = (500*scale, 600*scale)
		self.screen_width, self.screen_height = self.screensize

		pg.init()
		self.screen = pg.display.set_mode(self.screensize)
		pg.display.set_caption('Tic-Tac-Toe 2.0')

		self.FPS = 30
		self.FramePerSec = pg.time.Clock()

		self.pages = [
			startpage.StartPage(self, self.screen, game), 
			gamepage.GamePage(self, self.screen, game), 
			statspage.StatsPage(self, self.screen, game),
			infopage.InfoPage(self, self.screen, game)
			]
		self.set_page(0)

		self.visual_update_loop()

	def visual_update_loop(self):
		while True:
			events = pg.event.get()
			for event in events:
				if event.type == QUIT:
					pg.quit()
					sys.exit('\nProgram shutdown')
			self.current_page.update(events)
			pg.display.update()
			self.FramePerSec.tick(self.FPS)

	def set_page(self, index):
		self.current_page = self.pages[index]