import os
import pickle

class Themes:
    initialized_themes = {}
    def init_themes():
        for file_name in os.listdir('./src/gui_base/themes'):
            if file_name == 'theme_dict.py' or os.path.isdir(f'./src/gui_base/themes/{file_name}'):
                continue

            name, extension =  file_name.split('.')
            if extension != 'pickle':
                raise Exception('WARNING: failed to initilaize themes\nERROR: invalid fileformat for theme file, must use .pickle file extension')

            with open(f'./src/gui_base/themes/{name}.{extension}', 'rb') as theme:
                theme = pickle.load(theme)
            Themes.initialized_themes[theme[0]] = theme[1]
            
    def create_themes(dict):
        for item in dict.items():
            with open(f'./src/gui_base/themes/{item[0]}.pickle', 'wb') as theme:
                pickle.dump(item, theme, protocol = pickle.HIGHEST_PROTOCOL)

d = {
    'framed': {
        'font': 'Corbel', 
        'fontsize': 20, 
        'font colour': (255, 249, 232), 
        'background colour': (100, 50, 60), 
        'background size': (155, 54), 'background marginal': 0, 
        'rounded colour': (200, 100, 100), 'rounded true marginal': 10
        }, 
    'standard': {
        'font': 'Corbel', 
        'fontsize': 100, 
        'font colour': (200, 100, 100), 
        'background colour': (255, 249 , 232), 
        'background size': None, 
        'background marginal': 0, 
        'rounded colour': None, 
        'rounded true marginal': 0
        }
    }
Themes.create_themes(d)
#print(Themes.initialized_themes)
Themes.init_themes()