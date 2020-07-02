'''
        This is writing scene of game. GameScene must:
                - Start BG, Map, Game
                - Get players from Game
                -
'''
from __future__ import division, print_function, unicode_literals
# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
#

from cocos.scene import Scene
import cocos
from background import Background
from mapgame import Map
from game import Game
from pyglet.window import key
n = 9
size = (70*n, 70*n)

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.add(Background(size))
        self.add(Map(size, n))
        self.add(Game(size), name="game")

    def get_game_object(self):
        return self.get("game").get_children()

cocos.director.director.init(width =size[0],height =size[1])
cocos.director.director.run(GameScene())
