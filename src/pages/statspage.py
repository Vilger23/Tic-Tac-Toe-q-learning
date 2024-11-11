from src.gui_base.gui_framework import *
from src.pages.page_template import Page
import math
import time


class StatsPage(Page):
    def __init__(self, GUI, screen, game):
        super().__init__(GUI, screen, game)

        self.title = Text(self.handler, self.screen, text = 'COMING SOON', pos = (self.GUI.screen_width//(2*self.GUI.scale), self.GUI.screen_height//(2.8*self.GUI.scale)), bold = True)
        self.title.set_fontsize(63).set_background_colour(None)

        b = Button(self.handler, self.screen, 'change_gui_state', 0, '<-', pos = (self.GUI.screen_width // 2 / self.GUI.scale, self.GUI.screen_height // 1.7 / self.GUI.scale), theme = 'framed')
        b.inflate_background_size(-150, 0).set_scale_value(0.9).set_fontsize(20).align('center')

    def update(self, events):
        self.screen.fill( (255, 249 , 232) )
        super().update(events)