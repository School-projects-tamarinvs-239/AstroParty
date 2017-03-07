from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
#

import cocos
import cocos.director
from math import sin, cos, pi
from pyglet.window import key
from cocos.actions.interval_actions import RotateTo,MoveBy,Delay
from cocos.actions.instant_actions import CallFunc,Repeat


class MainScene(cocos.scene.Scene):
	def __init__(self):
		super().__init__()
		self.bg=cocos.layer.util_layers.ColorLayer(150,150,150,0,200,200)
		self.bg.position=(0,0)
		self.add(self.bg)
		self.add(Player())
	
class Player(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self):
		super().__init__()
		self.sprite = cocos.sprite.Sprite("test.jpg")
		self.sprite.position=(200,200)
		self.add(self.sprite)
		self.rot = 0
		self.bomb = 3
		self.keys=set()
		
		self.xmax=1200
		self.xmin=10
		self.ymax=710
		self.ymin=10
		self.v=7000
		self.maxbomb=3
		self.timereload=10
		
		self.sprite.do(Repeat(CallFunc(self.phizic)+Delay(0.001)))
		
	def reload(self):
		
		self.bomb += 1
		if self.bomb < self.maxbomb :
			self.sprite.do(Delay(self.timereload)+CallFunc(self.reload))
		print('+++')
	def on_key_release(self, keys, mod):
		# LEFT: выстрел
		# RIGTH: поворот
		self.keys.remove(keys)
		
		
		
	def on_key_press(self, keys, mod):
		# LEFT: выстрел
		# RIGTH: поворот
		self.keys.add(keys)
		
		#BOMB
		
		if key.LEFT in self.keys:
			if self.bomb == self.maxbomb:
				self.sprite.do(Delay(self.timereload)+CallFunc(self.reload))
			if self.bomb > 0 :
				self.bomb -= 1
				x, y = self.sprite.position
				self.add(Pula(self.v,self.rot,x,y))
				print("left",self.bomb)
			
		
	def phizic(self):
		deltarot=0.1
		timerot=0.01
		x, y = self.sprite.position
		if key.RIGHT in self.keys:
			self.rot = self.rot +deltarot
			print("right",self.rot)
		Vx = self.v*sin(self.rot)
		Vy = self.v*cos(self.rot)
		
		
		if x+Vx*0.001<self.xmax and x+Vx*0.001>self.xmin:
			x = x+Vx*0.001
		if y+Vy*0.001<self.ymax and y+Vy*0.001>self.ymin:
			y = y+Vy*0.001
		self.sprite.position = x, y
		self.sprite.rotation = (self.rot*(180/pi))
		
		
class Pula (cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self,v,rot,x,y):
		super().__init__()
		self.pula = cocos.sprite.Sprite("kramnik.jpg")
		self.v0=v*2.5
		self.rot=rot
		
		self.boom(v,rot,x,y)
	def boom (self,v,rot,x,y):
		self.pula.position=(x,y)
		self.add(self.pula) 
		
		self.pula.do(Repeat(CallFunc(self.phizic)+Delay(0.001)))
	def phizic (self):
		
		Vx = self.v0*sin(self.rot)
		Vy = self.v0*cos(self.rot)
		x, y = self.pula.position
		
		
		self.pula.position = x+Vx*0.001,y+Vy*0.001
		
			
cocos.director.director.init(width =1200,height =720)
cocos.director.director.run(MainScene())
