'''
        This file is writing bonus. Bonus must:
                - if it was killing by bullet open bonus
                - revers
'''
from cocos.sprite import Sprite
from random import randint

class Bonus(Sprite):
    def __init__(self,bonus, x, y):
        '''
            Parameters:
                    bonus : name of file (bonus.png / revers.png)
                    x, y : coordinats
        '''
        super().__init__(bonus)
        self.bonus = bonus[0:-4]
        self.position = x, y

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
        print('boom-bonus')
    def player_coordinat (self):
        if self.parent.PLAYER > 0:
            red = self.parent.get ("red")
            return  red.get_coordinat()
        else:
            return (0, 0 )
    def phizic (self, dt):
        typies = ['revers']
        x, y = self.position
        a, b = self.player_coordinat()
        start = False
        if abs(x - a) + abs(y - b) <= (35 + 30):
            start = True
        if start == True:
            #Choise type
            if self.bonus == 'bonus':
                l=int(len (typies))
                num = randint(0,l-1)
                self.parent.remove(self)
                self.make_bonus(x, y, typies[num])
            if self.bonus == 'revers':
                self.parent.sign *= -1
                self.parent.remove(self)
    def make_bonus (self, x, y, type):
        namefile = 'img/' + str(type) + '.png'
        self.parent.add(Bonus(namefile, x, y))
