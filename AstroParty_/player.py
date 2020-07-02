"""
Это файл, описывающий игрока. Игрок должен:
        - Летать
        - Стрелять
"""

from cocos.sprite import Sprite
from bullet import Bullet
from pyglet.window import key
from math import pi, sin, cos

class Player(Sprite):
    def __init__(self, player, controls, x, y, rot=0):
        """
        Параметры:
                player: имя файла с картинкой для этого игрока
                x, y, rot : coordinats and rotation
                controls: словарь {действие -> кнопка}
        """
        super().__init__(player)
        self.rot = rot/180*pi
        self.position = x, y
        self.controls = controls
        self.rotation = (self.rot*(180/pi))

        self.v=4
        self.maxbullet=3
        self.timereload=4
        self.bullet = 3
        self.keys=set()
        self.stop_x = False
        self.stop_y = False

        self.schedule(self.phizic)
    def collision_wall(self, int_coord):
        x, y = self.position
        dist_x = x - int_coord[0]
        dist_y = y - int_coord[1]
        if dist_x >= abs(dist_y ) or -1*dist_x >= abs(dist_y ):
            self.stop_x = True
        if dist_y >= abs(dist_x ) or -1*dist_y >= abs(dist_x ):
            self.stop_y = True
        print('boom-player')
    def get_coordinat(self):
        return self.position
    def reload(self, dt):
        self.bullet += 1
        if self.bullet >= self.maxbullet :
            self.unschedule(self.reload)

    def add_bullet (self):
        if self.bullet == self.maxbullet:
            self.schedule_interval(self.reload, self.timereload)
        if self.bullet > 0 :
            self.bullet -= 1
            x, y = self.position
            dx = 35*sin(self.rot)
            dy = 35*cos(self.rot)
            self.parent.add(Bullet(x + dx, y + dy, self.v, self.rot))
    def phizic(self, dt):
        deltarot=0.1
        x, y = self.position
        sign = self.parent.sign
        if  self.controls['turn'] in self.keys:
            self.rot = self.rot + sign*deltarot
        Vx = 0
        Vy = 0
        if self.stop_x != True:
            Vx = self.v*sin(self.rot)
        if self.stop_y != True:
            Vy = self.v*cos(self.rot)
        x, y = x + Vx, y + Vy
        self.stop_x = False
        self.stop_y = False
        #Изменение координат и угла
        self.position = x, y
        self.rotation = (self.rot*(180/pi))
