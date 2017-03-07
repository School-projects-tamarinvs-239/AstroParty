from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
#
import cocos
import cocos.director
from math import sin, cos, pi
from random import randint
from pyglet.window import key
from cocos.actions.interval_actions import RotateTo,MoveBy,Delay
from cocos.actions.instant_actions import CallFunc,Repeat


class MainScene(cocos.scene.Scene):
	def __init__(self):
		super().__init__()
		self.bg=cocos.layer.util_layers.ColorLayer(150,150,150,0,200,200)
		self.bg.position=(0,0)
		self.add(self.bg)
		################################
		#Variable
		razmer = (1280 , 720)
		self.redcoordinat = (200, 200)
		self.bluecoordinat = razmer - self.redcoordinat 
		#--------------
		
class Player(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self,name):
		super().__init__()
		#Создание игроков
		if name =='red' :
			self.sprite = cocos.sprite.Sprite("red.jpg")
			self.sprite.position=self.parent.redcoordinat
		
			self.rot = 0
		if name == 'blue':
			self.sprite = cocos.sprite.Sprite("blue.jpg")
			self.sprite.position=self.parent.bluecoordinat
			self.rot = pi
		self.add(self.sprite)
		