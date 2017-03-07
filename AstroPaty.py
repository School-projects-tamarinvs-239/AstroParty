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
			#Начальное положение и угол поворота
			self.sprite.position=self.parent.redcoordinat
			self.rot = 0
		if name == 'blue':
			self.sprite = cocos.sprite.Sprite("blue.jpg")
			#Начальное положение и угол поворота
			self.sprite.position=self.parent.bluecoordinat
			self.rot = pi
		self.add(self.sprite)
		
		self.bomb = 3
		self.keys=set()
		
		self.xmax=1200
		self.xmin=10
		self.ymax=710
		self.ymin=10
		self.v=3000
		self.maxbomb=3
		self.timereload=5
		
		#Запускаем
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
				#Работа с выстрелом
				self.do(Delay(0.001))
				self.parent.add(Pula(self.v,self.rot,x,y))
				
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
		#Выдача координат директору
		if self.name == 'red':
			#import pdb; pdb.set_trace()
			self.parent.redcoords  = x , y
		if self.name == 'blue':
			self.parent.bluecords = x , y
		#Изменение координат и угла
		self.sprite.position = x, y
		self.sprite.rotation = (self.rot*(180/pi))
	
	
	class Pula (cocos.layer.Layer):
		def __init__(self,v,rot,x,y):
			super().__init__()
			#Создание пули
			self.pula = cocos.sprite.Sprite("kramnik.jpg")
			
			#Выдача скорости и поворота
			self.v0=v*2.5
			self.rot=rot
			#Вывод на экран
			self.pula.position=(x,y)
			self.add(self.pula)
			#Начинаем полет
			self.pula.do(Repeat(CallFunc(self.phizic)+Delay(0.001)))
		def phizic (self):
			#Изменение координат
			Vx = self.v0*sin(self.rot)
			Vy = self.v0*cos(self.rot)
			x, y = self.pula.position
			
			#Проверка расположения
			if x<=1200 and x>=10 and y<=710 and y>= 10 :
				self.pula.position = x+Vx*0.001,y+Vy*0.001
			else:
				self.parent.remove(self.pula)
				#self.parent.remove(self.parent.namebomb[self.num])
				
cocos.director.director.init(width =1200,height =720)
cocos.director.director.run(MainScene())