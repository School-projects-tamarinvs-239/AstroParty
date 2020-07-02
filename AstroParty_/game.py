'''
        This file is writing game. Game must:
                - Start Player, Bullet, Bonus
                - keys -> player
                - get_players
                - get_bullets
'''
from cocos.layer import Layer
from player import Player
from bonus import Bonus
from pyglet.window import key

#Varible

class Game(Layer):
    is_event_handler = True
    def __init__(self, size):
        super().__init__()
        self.sign = 1
        self.size = size
        self.controls_red = {'shoot':key.LEFT,'turn': key.RIGHT}
        self.controls_blue = {'shoot':key.D,'turn': key.A}
        self.CONTROL = list( self.controls_red.values()) + list( self.controls_blue.values())
        self.PLAYER = 0
        self.stop = 0

        self.players = []

        self.add(Bonus('img/bonus.png', 500, 500))

    def on_key_press (self, symbol, mod):
        if symbol in self.CONTROL:
            self.add_keys_player (symbol)
            self.add_bullet_player (symbol)
    def on_key_release (self, symbol, mod):
        if symbol == key.SPACE and self.stop !=1:
            self.add(Player('img/red.png',self.controls_red, 200, 200, 0), name = 'red')
            #self.add(Player('img/blue.png',self.controls_blue, self.size[0] - 200, self.size[1] - 500, 0), name = 'blue')

            self.PLAYER +=1
            self.stop = 1
        if symbol in self.CONTROL:
            self.remove_keys_player (symbol)
    def add_bullet_player (self, symbol):
        if symbol == self.controls_red['shoot']:
            player = self.get("red")
            player.add_bullet()
        if symbol == self.controls_blue['shoot']:
            player = self.get("blue")
            player.add_bullet()
    def remove_keys_player (self, symbol):
        if self.PLAYER == 1:
            player = self.get("red")
            player.keys.remove (symbol)
        if self.PLAYER == 2:
            player = self.get("red")
            player.keys.remove (symbol)

            player = self.get("blue")
            player.keys.remove (symbol)
    def add_keys_player (self, symbol):
        if self.PLAYER == 1:
            player = self.get("red")
            player.keys.add (symbol)
        if self.PLAYER == 2:
            player = self.get("red")
            player.keys.add (symbol)

            player = self.get("blue")
            player.keys.add (symbol)
