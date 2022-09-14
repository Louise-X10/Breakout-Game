from config import GameConfiguration
from breakout_modified import BreakoutGame
from json import load

class BunsenConfig(GameConfiguration):

    def get_color_map(self):
        return {"G": "#A9C353", "P": "#9E7A3F", "B": "#000000", "X": None}

    def get_color_matrix(self):
        return ['XGGGGGGGGGX',
                'BGBBBGBBBGB',
                'BBBGBBBGBBB',
                'GGBBBGBBBGG',
                'GGGGGGGGGGG',
                'GGGGGPGGGGG',
                'XGGGGGGGGGX']

    def outline_bricks(self):
        return False

config = BunsenConfig()
breakout = BreakoutGame(BunsenConfig())
breakout.start()