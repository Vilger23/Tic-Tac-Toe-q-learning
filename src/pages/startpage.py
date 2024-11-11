from src.gui_base.gui_framework import Text, Button
from src.pages.page_template import Page
import math
import time


class StartPage(Page):
    def __init__(self, GUI, screen, game):
        super().__init__(GUI, screen, game)

        self.title = Text(self.handler, self.screen, text = 'TIC TAC TOE', pos = (self.GUI.screen_width//(2*self.GUI.scale), self.GUI.screen_height//(4*self.GUI.scale)), bold = True)
        self.title.set_fontsize(63).set_background_colour(None)

        start_game = ('change_gui_state', 1, 'Start Game')
        quit       = ('quit',' ', 'Quit')
        train_ai   = ('train_ai', 1_000_000, 'Train AI')
        stats      = ('change_gui_state', 2, 'Stats')
        info       = ('change_gui_state', 3, 'Info')
        github     = ('open_link', 'https://github.com/Vilger23', 'Github')

        button_grid = [
            [start_game, train_ai],
            [info      , stats   ],
            [quit      , github  ],
        ]
        b_w = 139/self.GUI.scale
        b_h = 48 /self.GUI.scale
        top_left_x = self.non_scaled_scr_w/2 - (len(button_grid[0])*b_w +   self.non_scaled_pad)/2
        top_left_y = self.non_scaled_scr_h/2 - (len(button_grid   )*b_h + 2*self.non_scaled_pad)/2 + 1.5*b_h

        for r, row in enumerate(button_grid):
            for c, b_config in enumerate(row):
                if b_config is None:
                    continue
                action, action_input, text = b_config
                b = Button(self.handler, self.screen, action, action_input, text, theme = 'framed', bold = True)
                b.set_pos((top_left_x + c*(b_w + self.non_scaled_pad), top_left_y + r*(b_h + self.non_scaled_pad))).align('topleft')


        #b = Button(self.handler, self.screen, 'train_ai', 2000, 'Train AI', theme = 'framed', bold = True)
        #b.set_pos((self.GUI.screen_width/(2*self.GUI.scale), self.GUI.screen_height/(2*self.GUI.scale) + b.background_size[1]/self.GUI.scale + self.pad/self.GUI.scale)).set_scale_value(0.9)

    def title_animation(self):
        t = time.time()
        stiffness = 2.4
        scale_range = 0.2
        y = scale_range * math.cos(stiffness * t)
        self.title.set_scale_value(y + 1)

    def update(self, events):
        self.screen.fill( (255, 249 , 232) )
        self.title_animation()
        super().update(events)