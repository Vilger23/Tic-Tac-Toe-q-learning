from src.gui_base.gui_framework import *
from src.pages.page_template import Page


class GamePage(Page):
    def __init__(self, GUI, screen, game):
        super().__init__(GUI, screen, game)

        sz_x = (self.GUI.screen_width - self.pad*4)/(3*self.GUI.scale)
        sz_y = sz_x
        self.pad = self.pad / self.GUI.scale
        for y in range(3):
            for x in range(3):
                b = Button(self.handler, self.screen, 'make_action', 'temp', ' ', pos = ( (self.pad+sz_x)*x + self.pad, (self.pad+sz_y)*y + self.pad) )
                b.set_background_size(sz_x, sz_y).align('topleft')

        pos_y = (self.pad + sz_y)*3 + self.pad
        sz_y = (self.GUI.screen_height/self.GUI.scale - self.pad*5 - sz_y*3)
        for x, b in enumerate([('<-', 'change_gui_state', 0), ('Player1<AI', 'change_beginning_player', 'temp'),  ('Stats', 'change_gui_state', 2)]):
            
            b = Button(self.handler, self.screen, b[1], b[2], b[0], pos = ( (self.pad+sz_x)*x + self.pad, pos_y), theme = 'framed', bold = True)
            b.set_background_size(sz_x, sz_y).align('topleft')

    
    def update(self, events):
        self.screen.fill( (0, 0 , 50) )
        mouse_pos = pg.mouse.get_pos()
        left_click_up, left_click_down = False, False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                left_click_down = True
            if event.type == pg.MOUSEBUTTONUP:
                left_click_up = True

        for button, num in zip(self.handler.buttons, self.game.board):
            button.set_text(self.game.num_to_char[num])

        self.handler.update(mouse_pos, left_click_down, left_click_up)
        self.handler.display_objects()
