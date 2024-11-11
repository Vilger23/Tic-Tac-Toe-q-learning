import pygame as pg
from pygame.locals import *
import sys
import src.gui_base.themes.theme_dict as themes
from src.gui_base.objecthandler import ObjectHandler
text_theme = themes.Themes.initialized_themes


class Text:
    def __init__(self, handler, display, text = "Text here", pos = (0, 0), theme = "standard", bold = False):
        self.handler = handler
        self.handler.objects.append(self)
        self.gui_scale = self.handler.GUI.scale
        self.display = display
        self.text = text
        self.pos = tuple(map(lambda x:int(x*self.gui_scale), pos))
        self.posx, self.posy = self.pos
        self.theme = theme      
        self.bold = bold
        self.updated = False

        self.scale_value = 1*self.gui_scale
        self.base_scale = 1*self.gui_scale
        self.offsetx, self.offsety = 0, 0
        self.alignment = 'center'
        self.set_theme(self.theme)  

    def set_text(self, text_):
        self.text = text_
        self.update_visuals()
        return self

    def set_pos(self, pos_):
        self.pos = tuple(map(lambda x:int(x*self.gui_scale), pos_))
        self.posx, self.posy = self.pos
        self.update_visuals()
        return self

    def set_font(self, font_name_):
        self.font_name = font_name_
        self.init_font()
        return self

    def set_fontsize(self, fontsize_):
        self.fontsize = fontsize_*self.gui_scale
        self.init_font()
        return self

    def set_font_colour(self, font_colour_):
        self.font_colour = font_colour_
        self.update_visuals()
        return self

    def init_font(self):
        self.font = pg.font.SysFont(self.font_name, int(self.fontsize))
        if self.bold:
            self.font.bold = True
        self.update_visuals()
        return self

    def set_background_marginal(self, background_size_multiplier_):
        self.background_marginal = background_size_multiplier_*self.gui_scale
        self.update_visuals()
        return self

    def set_background_colour(self, background_colour_):
        self.background_colour = background_colour_
        self.update_visuals()
        return self

    def inflate_background_size(self, inflation_x_, inflation_y_):
        inflation = (inflation_x_, inflation_y_)
        self.inflation_x, self.inflation_y = map(lambda x: int(x*self.gui_scale), inflation)
        self.update_visuals()
        return self

    def set_background_size(self, bg_width, bg_height):
        self.background_size = int(bg_width*self.gui_scale), int(bg_height*self.gui_scale)
        self.update_visuals()
        return self

    def set_scale_value(self, scale_value_):
        self.base_scale*=(scale_value_/self.scale_value)*self.gui_scale
        self*(scale_value_/self.scale_value)*self.gui_scale
        return self

    def reset_scale(self):
        self*(self.base_scale/self.scale_value)

    def align(self, alignment):
        self.alignment = alignment
        self.calculate_offset()
        self.update_visuals()
        return self

    def calculate_offset(self):
        offset_chart = {
            'topleft': (1, 1),
            'top': (0, 1),
            'topright': (-1, 1),
            'right': (-1, 0),
            'bottomright': (-1, -1),
            'bottom': (0, -1),
            'bottomleft': (1, -1),
            'left': (1, 0),
            'center': (0, 0)
        }
        x_mp, y_mp = offset_chart[self.alignment]
        self.offsetx, self.offsety = self.background_size[0]*x_mp/2, self.background_size[1]*y_mp/2
        return self

    '''sets object variables to '''
    def set_theme(self, theme):
        self.font_name             =     text_theme[theme]['font'                 ]
        self.fontsize              = int(text_theme[theme]['fontsize'             ]*self.gui_scale)
        self.font_colour           =     text_theme[theme]['font colour'          ]
        self.rounded_colour        =     text_theme[theme]['rounded colour'       ]
        self.rounded_true_marginal = int(text_theme[theme]['rounded true marginal']*self.gui_scale)
        self.background_marginal   = int(text_theme[theme]['background marginal'  ]*self.gui_scale)        
        self.background_colour     =     text_theme[theme]['background colour'    ]

        self.theme = theme
        try:
            self.background_size   = tuple(map(lambda x:int(x*self.gui_scale), text_theme[theme]['background size']))
        except:
            self.background_size = None
        self.init_font()
        return self

    '''Calculates the necessary information for visualising the object. It is seperate from display_visuals(), 
    the idea being that you do not have to make the calculations for every frame'''
    def update_visuals(self):
        text_surface = self.font.render(self.text, True, self.font_colour)
        self.text_surface, self.text_rect = text_surface, text_surface.get_rect()
        self.width, self.height = self.text_rect.size

        if not self.background_size or not self.background_colour:
            self.background_size = self.text_rect.size

        self.center_pos = ( self.posx + self.offsetx, self.posy + self.offsety)
        self.text_rect.center = self.center_pos

        if self.background_marginal:
            true_marginal = self.height*self.background_marginal
            self.background_size = self.width + 2*true_marginal, self.height + 2*true_marginal

        self.background_rect = pg.Rect(self.center_pos, self.background_size)
        self.background_rect.center = self.center_pos
        self.updated = True

    '''displays the pre-calculated visuals on the screen'''
    def display_visuals(self):
        
        if self.background_colour: 
            self.display_background()
        if self.rounded_colour:
            self.display_frame()
        self.display.blit(self.text_surface, self.text_rect)

    '''displays background'''
    def display_background(self):
        pg.draw.rect(self.display, self.background_colour, self.background_rect)

    '''calculates and displays rounded background, creating "framed" effect'''
    def display_frame(self):
        bg_width, bg_height = self.background_size
        rounded_size = bg_width - 2*self.rounded_true_marginal, bg_height - 2*self.rounded_true_marginal
        rounded_rect = pg.Rect(self.center_pos, rounded_size)
        rounded_rect.center = self.center_pos
        pg.draw.rect(self.display, self.rounded_colour, rounded_rect, 0, int(self.rounded_true_marginal))

    '''causes the visuals to scale when the object is multiplied with an integer'''
    def __mul__(self, other):
        self.fontsize*=other
        self.rounded_true_marginal*=other
        self.scale_value*=other
        bg_width, bg_height = self.background_size
        self.background_size = bg_width * other, bg_height * other
        self.init_font()
        return self
        
class Button(Text):
    def __init__(self, handler, display, action, action_input, text = "button", pos = (0, 0), theme = "standard", bold = False):
        super().__init__(handler, display, text, pos, theme, bold)

        '''button specific'''
        handler.buttons.append(self)
        self.action = getattr(ObjectHandler, action)
        if not self.background_colour:
            self.background_colour = (100, 100, 140)
        self.action_input = action_input
        self.is_clicked = False
        self.hover_multiplier = 1.04
        self.bio = {action: 0}

    def mouse_collision(self, point, left_click_down, left_click_up):
        '''check if mouse collides with button'''
        collision = self.background_rect.collidepoint(point)
        '''Scales button as a visual que'''
        self.reset_scale()
        if collision:
            self*self.hover_multiplier
        else:
            self.is_clicked = False
            return

        '''calles the clicked function if it is clicked'''
        if left_click_down:
            self.action(self, self.action_input)
            self.is_clicked = True
        if left_click_up:
            self.is_clicked = False

        if self.is_clicked:
            self*0.9

