'''
        This is writing map. Map must:
                - Make map +
                - Check collisions this players, bullets
'''

from cocos.layer import Layer
from cocos.sprite import Sprite
from open_file_map import open_file

class Map(Layer):
    def __init__(self, size, n):
        '''
                Parametrs:
                        size - size map
                        n - calc n*n
        '''
        super().__init__()
        self.n = n
        self.make_map(size)

        self.schedule(self.collision)

    def make_map(self,size,model = 'along the border'):
        null = 0 , 0
        self.tail = []
        self.wall = []
        f = open_file('map1.txt')
        text = str(f[0])
        x, y = 0, 0
        for i in text:
            if i != '\n' and i == '+':
                self.tail.append ((null[0] + x*70,  null[1] + y*70))
            elif i == '\n':
                x = 0
                y += 1
            x += 1

        for t in self.tail:
            number = len(self.wall)
            self.wall.append (Sprite('img/wall.png'))
            self.wall[number].position = t
            self.add(self.wall[number])
    def collision(self, dt):
        self.objects = self.parent.get_game_object()
        #print(self.objects)
        for obj in self.objects:
            x, y = obj.get_coordinat()
            dx = 0
            dy = 0
            if x%70 >= 35 :
                dx += 70
            if y%70 >= 35 :
                dy += 70
            int_coord = (x//70)*70 + dx, (y//70)*70 + dy
            if int_coord in self.tail:
                obj.collision_wall(int_coord)
