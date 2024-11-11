from src.gui_base.objecthandler import ObjectHandler
import pygame as pg

class Page():
    def __init__(self, GUI, screen, game):
        self.GUI = GUI
        self.game = game
        self.screen = screen
        self.pad = 12*GUI.scale
        self.non_scaled_scr_w = self.GUI.screen_width/self.GUI.scale
        self.non_scaled_scr_h = self.GUI.screen_height/self.GUI.scale
        self.non_scaled_pad   = self.pad/self.GUI.scale
        self.handler = ObjectHandler(game, GUI, self.pad)

    def update(self, events):
        mouse_pos = pg.mouse.get_pos()
        left_click_up, left_click_down = False, False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                left_click_down = True
            if event.type == pg.MOUSEBUTTONUP:
                left_click_up = True

        self.handler.update(mouse_pos, left_click_down, left_click_up)
        self.handler.display_objects()