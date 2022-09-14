from config import GameConfiguration
from breakout import BreakoutGame
from json import load

class ClassicConfig(GameConfiguration):

    def get_color_map(self):
        return {"O": "orange", "G": "green", "B": "blue",
                "R": "red", "C": "cyan"}

    def get_color_matrix(self):
        return ['R'*10, 'R'*10, 'O'*10, 'O'*10, 'G'*10, 'G'*10,
                'C'*10, 'C'*10, 'B'*10, 'B'*10]


config = ClassicConfig()
breakout = BreakoutGame(ClassicConfig())
breakout.start()