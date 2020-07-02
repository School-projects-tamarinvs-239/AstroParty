'''
        This file is writing bullet. Bullet must:
                - Fly
'''
from cocos.sprite import Sprite
from math import sin, cos

class Bullet(Sprite):
    def __init__(self, x, y, v, rot):
        '''
                Parameters:
                        x, y : coordinats
                        v : speed of player
                        rot : rotation
        '''
        super().__init__('img/bullet.png')
        #Выдача скорости и поворота
        self.v0=v*2.5
        self.rot=rot
        #Вывод на экран
        self.position= x, y
        #Начинаем полет
        self.schedule(self.phizic)
    def get_coordinat(self):
        return self.position
    def collision_wall(self, int_coord):
        x, y = self.position
        dist_x = x - int_coord[0]
        dist_y = y - int_coord[1]
        if dist_x >= abs(dist_y ) or -1*dist_x >= abs(dist_y ):
            self.stop_x = True
        if dist_y >= abs(dist_x ) or -1*dist_y >= abs(dist_x ):
            self.stop_y = True
        print('boom-bullet')
    def phizic (self, dt):
        Vx = self.v0*sin(self.rot)
        Vy = self.v0*cos(self.rot)
        x, y = self.position
        x, y = x + Vx, y + Vy
        self.position = x, y

