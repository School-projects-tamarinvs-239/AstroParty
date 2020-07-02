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
		self.keys={key.LEFT:0,key.RIGHT:0}
		
		self.xmax=1900
		self.xmin=10
		self.ymax=1070
		self.ymin=10
		
		#self.coordinat={x:50,y:60}
		self.sprite.do(Repeat(CallFunc(self.Param)+Delay(0.001)))
	def on_key_release(self, keys, mod):
		# LEFT: выстрел
		# RIGTH: поворот
		self.keys[keys] = 0
	def on_key_press(self, keys, mod):
		# LEFT: выстрел
		# RIGTH: поворот
		self.keys[keys] = 1
		
		
	def Param(self):
		v=10000
		deltarot=0.1
		timerot=0.05
		if self.keys[key.RIGHT]==1:
			self.rot = self.rot +deltarot
			print("right",self.rot)
		if self.keys[key.LEFT]==1:
			self.bomb = self.bomb - 1
			x, y = self.sprite.position
			self.add(Pula(v,self.rot,x,y))
			if self.bomb <= 0:
				self.bomb = 0
			if self.bomb >= 3:
				self.bomb = 3
			print("left",self.bomb)
		Vx = v*sin(self.rot)
		Vy = v*cos(self.rot)
		x, y = self.sprite.position
		
		"""
		if x+Vx > self.xmax :
			Vx = self.xmax - x 
		if x+Vx < self.xmin :
			Vx = self.xmin - x 
		if y+Vy > self.ymin :
			Vy = self.ymax - y 
		if y+Vy < self.ymin :
			Vy = self.ymin - y 
		"""
		if x+Vx*0.001<self.xmax and x+Vx*0.001>self.xmin:
			x = x+Vx*0.001
		if y+Vy*0.001<self.ymax and y+Vy*0.001>self.ymin:
			y = y+Vy*0.001
		self.sprite.position = x,y
		self.sprite.rotation = self.rot*180/pi
		#if ((self.coordinat[x]+1*sin(self.rot))in[0,600]) and ((self.coordinar[y]+1*cos(self.rot)) in [0,600]):
		#	self.coordinat[x]+=1*sin(self.rot)
		#	self.coordinar[y]+=1*cos(self.rot)
		#self.sprite.do(RotateTo((self.rot*180/pi), timerot)+MoveBy((10*sin(self.rot),10*cos(self.rot)),v))
		
		
class Pula (cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self,v,rot,x,y):
		super().__init__()
		self.pula = cocos.sprite.Sprite("kramnik.jpg")
		self.v0=v*2
		self.rot=rot
		self.boom(v,rot,x,y)
	def boom (self,v,rot,x,y):
		self.pula.position=(x,y)
		self.add(self.pula) 
		
		self.pula.do(Repeat(CallFunc(self.param)+Delay(0.001)))
	def param (self):
		
		Vx = self.v0*sin(self.rot)
		Vy = self.v0*cos(self.rot)
		x, y = self.pula.position
		self.pula.position = x+Vx*0.001,y+Vy*0.001
cocos.director.director.init(width =1980,height =1080)
cocos.director.director.run(MainScene())
