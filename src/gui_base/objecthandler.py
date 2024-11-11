import sys
import os
import pygame as pg
import webbrowser

class ObjectHandler():
    def __init__(self, game, GUI, padding):
        self.game = game
        self.GUI = GUI
        self.objects = []
        self.buttons = []
        self.line = ''
        self.padding = padding

    def display_objects(self):
        for obj in self.objects:
            obj.display_visuals()

    def update(self, mouse_pos_, left_click_down, left_click_up):
        self.update_buttons(mouse_pos_, left_click_down, left_click_up)

    def update_buttons(self, mouse_pos_, left_click_down, left_click_up):
        for obj in self.buttons:
            obj.mouse_collision(mouse_pos_, left_click_down, left_click_up)

    '''methods triggered by buttons'''
    def change_gui_state(self, index):
        self.handler.GUI.set_page(index)

    def quit(self, temp):
        pg.quit()
        sys.exit()

    def change_beginning_player(self, temp):
        self.handler.game.ai_starting = True if self.handler.game.ai_starting == False else False
        num_to_text = {False: 'Player1<AI', True: 'Player1>AI'}
        self.set_text(num_to_text[self.handler.game.ai_starting])

    def train_ai(self, epochs):
        os.system(f'python train_ai.py --epochs {epochs}')

    def open_link(self, url):
        webbrowser.open(url, new=0, autoraise=True)

    def make_action(self, temp):
        ix = self.posx // (self.handler.padding + self.background_size[0])
        iy = self.posy // (self.handler.padding + self.background_size[0])
        oned_i = int(iy*3 + ix)
        a = [0,]*9
        a[oned_i] = self.handler.game.current_player
        if not self.handler.game.board[oned_i]:
            self.handler.game.action(tuple(a))