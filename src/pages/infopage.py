from src.gui_base.gui_framework import *
from src.pages.page_template import Page
import math
import time


class InfoPage(Page):
    def __init__(self, GUI, screen, game):
        super().__init__(GUI, screen, game)
        model_data = self.game.ai.current_model.split('%')[1:-1]
        model_data = [*map(lambda x:float(x.split('=')[1]), model_data)]

        title_pos = (self.non_scaled_pad, self.non_scaled_scr_w-148) 

        self.title = Text(self.handler, self.screen, text = 'Current AI-model spec', pos = title_pos, bold=True)
        self.title.set_fontsize(20).set_background_colour(None).align('left')

        txt1_pos = (title_pos[0], title_pos[1] + 1*(self.pad + self.title.height/self.GUI.scale))

        self.txt1 = Text(self.handler, self.screen, text = f'Iterations trained: {int(model_data[3])}'     , pos = txt1_pos)
        self.txt1.set_fontsize(20).set_background_colour(None).align('left')

        self.txt2 = Text(self.handler, self.screen, text = f'Learning rate: {model_data[0]*100}%'   , pos = (txt1_pos[0], txt1_pos[1] + 1*(self.pad + self.txt1.height/self.GUI.scale)))
        self.txt2.set_fontsize(20).set_background_colour(None).align('left')   

        self.txt3 = Text(self.handler, self.screen, text = f'Exploration rate: {model_data[1]*100}%', pos = (txt1_pos[0], txt1_pos[1] + 2*(self.pad + self.txt1.height/self.GUI.scale)))
        self.txt3.set_fontsize(20).set_background_colour(None).align('left')

        self.txt4 = Text(self.handler, self.screen, text = f'Gamma value: {model_data[2]}'          , pos = (txt1_pos[0], txt1_pos[1] + 3*(self.pad + self.txt1.height/self.GUI.scale)))
        self.txt4.set_fontsize(20).set_background_colour(None).align('left')

        self.title1 = Text(self.handler, self.screen, text = 'General information', pos = (self.non_scaled_pad, 2*self.non_scaled_pad), bold=True)
        self.title1.set_fontsize(20).set_background_colour(None).align('left')

        self.lines = (
            'The purpose of this project was to program a Tic-Tac-Toe', 
            'bot with near optimal play. This is traditionally done',
            'with a min-max algorithm, but I wanted to try and',
            'experiment with Q-learning algorithms. The AI is trained',
            'against it self where each state-action pair it encounters',
            'is saved. When the bot reaches an end state the appropiate',
            'reward is back-propogated through the saved state-action',
            'pairs, given by:',
            'Q(s,a) = Q(s,a) + alpha*(gamma*reward - Q(s,a))'
            )

        for i, line in enumerate(self.lines):
            t = Text(self.handler, self.screen, text = line, pos = (self.title1.pos[0]/self.GUI.scale, (self.title1.pos[1] + self.title.height + self.pad)/self.GUI.scale + i*(self.pad+self.txt1.height)/self.GUI.scale))
            t.set_fontsize(20).set_background_colour(None).align('left')


        #print(sum(map(lambda x: (x.height + self.pad)/self.GUI.scale, self.handler.objects))-self.non_scaled_pad)

        b = Button(self.handler, self.screen, 'change_gui_state', 0, '<-', pos = (self.GUI.screen_width // 2 / self.GUI.scale, self.non_scaled_scr_h - 50), theme = 'framed')
        b.set_scale_value(0.9).set_fontsize(20)

    def update(self, events):
        self.screen.fill( (255, 249 , 232) )
        super().update(events)