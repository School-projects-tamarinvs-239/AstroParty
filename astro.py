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
		self.add(Player('red'))
		self.add(Player('blue'))
		self.namebomb=[]
		self.num=0
		
		self.redcoords = (200, 200)
		self.bluecoords = (1080, 520)
		
	def plusbomb(self,number):
		n=''
		for i in range (1,number+1):
			n+='a'
		self.namebomb.append(n)
	
		 
class Player(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self,name):
		super().__init__()
		if name =='red' :
			self.sprite = cocos.sprite.Sprite("red.jpg")
			self.sprite.position=(200,200)
			
			self.rot = 0
		if name == 'blue':
			self.sprite = cocos.sprite.Sprite("blue.jpg")
			self.sprite.position=(1280-200,720-200)
			self.rot = pi
		self.add(self.sprite)
		self.name=name;
		self.bomb = 3
		self.keys=set()
		
		self.xmax=1200
		self.xmin=10
		self.ymax=710
		self.ymin=10
		self.v=3000
		self.maxbomb=3
		self.timereload=5
		
		sprite.do(ScaleTo(500, 2))
		
		self.sprite.do(Repeat(Delay(0.001)+CallFunc(self.phizic)))
		
	def reload(self):
		
		self.bomb += 1
		if self.bomb < self.maxbomb :
			self.sprite.do(Delay(self.timereload)+CallFunc(self.reload))
		
	def on_key_release(self, keys, mod):
		# LEFT: выстрел
		# RIGTH: поворот
		self.keys.remove(keys)
		
		
		
	def on_key_press(self, keys, mod):
		# LEFT,a: выстрел
		# RIGTH,d: поворот
		self.keys.add(keys)
		
		#BOMB
		if (key.LEFT in self.keys and self.name=='red')or (key.A in self.keys and self.name=='blue'):
			if self.bomb == self.maxbomb:
				self.sprite.do(Delay(self.timereload)+CallFunc(self.reload))
			if self.bomb > 0 :
				self.bomb -= 1
				x, y = self.sprite.position
				self.parent.num+=1
				n=self.parent.num -1
				
				self.parent.plusbomb(n)
				print(self.parent.namebomb,n)
				namep = self.parent.namebomb[n]
				self.do(Delay(0.001))
				self.parent.add(Pula(self.v,self.rot,x,y,namep,n),name=namep)
				
				
			
		
	def phizic(self):
		deltarot=0.1
		timerot=0.01
		x, y = self.sprite.position
		if (key.RIGHT in self.keys and self.name=='red') or (key.D in self.keys and self.name=='blue'):
			self.rot = self.rot +deltarot
			
		Vx = self.v*sin(self.rot)
		Vy = self.v*cos(self.rot)
		
		
		if (x+Vx*0.001<self.xmax) and (x+Vx*0.001>self.xmin):
			x = x+Vx*0.001
		if (y+Vy*0.001<self.ymax) and (y+Vy*0.001>self.ymin):
			y = y+Vy*0.001
			
		if self.name == 'red':
			#import pdb; pdb.set_trace()
			self.parent.redcoords  = x , y
		if self.name == 'blue':
			self.parent.bluecords = x , y
		
		self.sprite.position = x, y
		self.sprite.rotation = (self.rot*(180/pi))
		
		
class Pula (cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self,v,rot,x,y,namep,num):
		super().__init__()
		
		self.pula = cocos.sprite.Sprite("kramnik.jpg")
		
		
		self.v0=v*2.5
		self.rot=rot
		self.namep=namep
		self.num=num
		
		self.pula.position=(x,y)
		self.add(self.pula)
		
		self.pula.do(Repeat(CallFunc(self.phizic)+Delay(0.001)))
	def phizic (self):
		
		Vx = self.v0*sin(self.rot)
		Vy = self.v0*cos(self.rot)
		x, y = self.pula.position
		
		if x<=1200 and x>=10 and y<=710 and y>= 10 :
			self.pula.position = x+Vx*0.001,y+Vy*0.001
		else:
			self.parent.remove(self.pula)
			#self.parent.remove(self.parent.namebomb[self.num])
			
cocos.director.director.init(width =1200,height =720)
cocos.director.director.run(MainScene())
