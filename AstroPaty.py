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
from cocos.actions.interval_actions import RotateTo,MoveBy,Delay,ScaleTo
from cocos.actions.instant_actions import CallFunc,Repeat


class MainScene(cocos.scene.Scene):
	def __init__(self):
		super().__init__()
		self.bg=cocos.layer.util_layers.ColorLayer(150,150,150,0,200,200)
		self.bg.position=(0,0)
		self.add(self.bg)
		#Фон
		self.add(Phon())
		################################
		#Variable
		razmer = (900 , 900)
		self.redcoordinat = (400, 400)
		self.bluecoordinat = razmer[0] - self.redcoordinat[0], razmer[1] - self.redcoordinat[1]
		#--------------
		self.add(Player('red',self.redcoordinat,razmer ))

class Phon (cocos.layer.Layer):
	def __init__(self):
		super().__init__()
		self.phon = cocos.sprite.Sprite("phon.jpg")
		self.phon.position=(450,450)
		self.add(self.phon)
class Player(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self,name,pos,razmer):
		super().__init__()
		#Создание игроков
		if name =='red' :
			self.sprite = cocos.sprite.Sprite("red.jpg")
			#Начальное положение и угол поворота
			self.sprite.position=pos
			self.rot = 0
			
			
		if name == 'blue':
			self.sprite = cocos.sprite.Sprite("blue.jpg")
			#Начальное положение и угол поворота
			self.sprite.position=pos
			self.rot = pi
		self.add(self.sprite)
		self.sprite.do(ScaleTo(0.4, 0))
		self.name = name
		
		self.bomb = 3
		self.keys=set()
		
		#Граница поля, скорость, бомбы
		self.xmax=razmer[0]-30
		self.xmin=30
		self.ymax=razmer[1]-30
		self.ymin=30
		self.v=4
		self.maxbomb=3
		self.timereload=5
		
		#Запускаем
		self.sprite.do(Repeat(Delay(0.001)+CallFunc(self.phizic)))
		
	def reload(self):
		self.bomb += 1
		if self.bomb < self.maxbomb :
			self.sprite.do(Delay(self.timereload)+CallFunc(self.reload))
	def on_key_release(self, keys, mod):
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
		
		
		if (x+Vx<self.xmax) and (x+Vx>self.xmin):
			x = x + Vx
		if (y+Vy<self.ymax) and (y+Vy>self.ymin):
			y = y + Vy
		#Выдача координат директору
		if self.name == 'red':
			#import pdb; pdb.set_trace()
			self.parent.redcoordinat  = x , y
		if self.name == 'blue':
			self.parent.bluecoordinat = x , y
		#Изменение координат и угла
		self.sprite.position = x, y
		self.sprite.rotation = (self.rot*(180/pi))
	
	
class Pula (cocos.sprite.Sprite):
	def __init__(self,v,rot,x,y):
		super().__init__("kramnik.jpg")
		
		#Выдача скорости и поворота
		self.v0=v*2.5
		self.rot=rot
		#Вывод на экран
		self.do(ScaleTo(0.4, 0))
		self.position=(x,y)
		#Начинаем полет
		self.do(Repeat(CallFunc(self.phizic)+Delay(0.001)))
	def phizic (self):
		#Изменение координат
		Vx = self.v0*sin(self.rot)
		Vy = self.v0*cos(self.rot)
		x, y = self.position
		
		#Проверка расположения
		if x<=890 and x>=10 and y<=890 and y>= 10 :
			self.position = x+Vx,y+Vy
		else:
			self.parent.remove(self)
			#self.parent.remove(self.parent.namebomb[self.num])
			
cocos.director.director.init(width =900,height =900)
cocos.director.director.run(MainScene())