from cocos.sprite import Sprite
from cocos.layer import Layer
from cocos.layer.util_layers import ColorLayer

class Background(Layer):
    def __init__(self,size):
        super().__init__()
        self.bg=ColorLayer(150,150,150,0,200,200)
        self.bg.position=(0,0)
        self.add(self.bg)
        self.phon = Sprite('img/phon.png')
        self.phon.position = (size[0]/2 , size[1]/2)
        self.add(self.phon)
