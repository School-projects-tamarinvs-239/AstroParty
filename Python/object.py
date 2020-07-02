from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))
#
import cocos
import cocos.director
from math import sin, cos, pi, sqrt
from random import randint
from pyglet.window import key
from cocos.actions.interval_actions import RotateTo,MoveBy,Delay,ScaleTo
from cocos.actions.instant_actions import CallFunc,Repeat

size = (700, 500)

class MainScene(cocos.scene.Scene):
	def __init__(self):
		super().__init__()
		self.bg=cocos.layer.util_layers.ColorLayer(150,150,150,0,200,200)
		self.bg.position=(0,0)
		self.add(self.bg)
		
		self.sign = 1
		self.object = []
		self.object_inf = []
		self.object_inf_future = []
		self.object_die_number = []
		self.object_die_now = []
		self.object_stop = {}
		self.R = {'Player':30,'Bonus':35,'Revers':40,'Pula':7.5,'Stena':35}
		
		#PHON
		self.phon = cocos.sprite.Sprite('phon.png')
		self.phon.position = (size[0]/2 , size[1]/2)
		self.add(self.phon)
		#inf + make object[0]
		#self.all_build_object('Player',100,400,90)
		self.all_build_object('Bonus',300,300)
		
		self.all_build_object('Stena',115,10,0,1)
		
		self.all_build_object('Stena',45,10,0,1)
		
		self.all_build_object('Player',100,100,0)
		
		self.do(Repeat(Delay(0.001)+CallFunc(self.CONTROL)))
	def all_build_object (self,vid,x,y,rot=0,form_sten=0):
		self.object_inform(vid,x,y,rot,form_sten)
		self.do(Delay(0.001))
		self.make_object (self.object_inf[len(self.object)],rot,form_sten)
	def object_inform (self,vid,x,y,rot=0,form_sten=0):
		if vid =='Player':
			self.object_inf.append  ((vid,x,y,rot))
			self.object_inf_future.append ((vid,x,y,rot))
		elif vid =='Stena':
			self.object_inf.append  ((vid,x,y,rot,form_sten))
			self.object_inf_future.append ((vid,x,y,rot,form_sten))
		else:
			self.object_inf.append  ((vid,x,y))
			self.object_inf_future.append ((vid,x,y))
		self.do(Delay(0.001))
	def make_object (self, inf,rot=0,form_sten=0):
		number = len (self.object) 
		if inf[0] == 'Player':
			for i in range(number):
				if self.object_inf[i][0] == 'Player':
					self.object.append(cocos.sprite.Sprite("blue.png"))
					self.add(Player(self.object[number],self.object_inf[number],'blue',number,rot))
					self.object_stop[number] = (0,)
					break
				else:
					self.object.append(cocos.sprite.Sprite("red.png"))
					self.add(Player(self.object[number],self.object_inf[number],'red',number,rot))
					self.object_stop[number] = (0,)
					break
			if number == 0: 
				self.object.append(cocos.sprite.Sprite("red.png"))
				self.add(Player(self.object[number],self.object_inf[number],'red',number,rot))
				self.object_stop[number] = (0,)
		if inf[0] =='Bonus':
			self.object.append(cocos.sprite.Sprite("bonus.png"))
			self.add(Bonus(self.object[number],self.object_inf[number],number))
		if inf[0] == 'Revers':
			self.object.append(cocos.sprite.Sprite("revers.png"))
			self.add(Bonus(self.object[number],self.object_inf[number],number))
		if inf[0] == 'Pula':
			self.object.append(cocos.sprite.Sprite("pula.png"))
			self.add(Pula(self.object[number],self.v,self.rot,inf,number))
		if inf[0] == 'Stena':
			if inf[4] == 1:
				name_stena = "stena.png"
			elif inf[4] == 2:
				name_stena = "stena_ugol.png"
			elif inf[4] == 3:
				name_stena = "stena_versh.png"
			self.object.append(cocos.sprite.Sprite(name_stena))
			rot=self.object_inf[number][3]
			self.add(Stena(self.object[number],self.object_inf[number],number,rot))
			
	def CONTROL (self):
		#print(self.object_inf)
		for num1 in range(len(self.object_inf)):
			if self.object_inf[num1][0] == 'None':
				continue
			for num2 in range(num1):
				if self.object_inf[num2][0] == 'None':
					continue
				
				#print(self.object_inf[num1],self.object_inf[num2])
				self.object_inf[num1] = self.object_inf_future[num1]
				self.object_inf[num2] = self.object_inf_future[num2]
				self.o1 = self.object_inf[num1]
				self.o2 = self.object_inf[num2]
				name1 = self.o1[0]
				name2 = self.o2[0]
				
				R1 = self.R[name1]
				R2 = self.R[name2]
				
				dist = sqrt ((self.o1[1]-self.o2[1])**2 + (self.o1[2]-self.o2[2])**2)
				
				s={name1,name2}
				
				if name1 in {'Player','Pula'} and name2 == 'Stena':
						name1 , name2 = name2, name1
						num1 , num2 = num2, num1
				if name2 in {'Player','Pula'} and name1 == 'Stena':
					#print(self.object_inf[num1])
					# first = Stena
					dist_y = abs(self.object_inf[num2][2]-self.object_inf[num1][2])
					dist_x = abs(self.object_inf[num2][1]-self.object_inf[num1][1])
					print(dist_y)
					if  (dist_x < R1+R2) or (dist_y < R1+R2) :
						self.happend (s,num1,num2)
				elif name1 != name2 and dist < R1+R2 :
					self.happend (s,num1,num2)
				
		self.object_die_now.sort(reverse = True)
		#print(self.object_die_now)
		for i in self.object_die_now:
			if self.object_die_now.count (i) > 1:
				del self.object_die_now[self.object_die_now.index(i)]
			if self.object_die_now.count (i) == 1:
				#print('=')
				self.die_object(i)
		del self.object_die_now[:]
		
	def happend (self, s,num1,num2):
		if s == {'Pula','Bonus'}:
			#print('-------',0)
			self.object_die_now.append(num1)
			self.object_die_now.append(num2)
		if s == {'Player','Revers'}:
			#print('-------',1)
			if self.object_inf[num1][0] == 'Revers':
				num = num1
			else:
				num = num2
			self.object_die_now.append(num)
		if s == {'Player','Stena'} :
			if self.object_inf[num1][0] == 'Stena':
				num1, num2 = num2, num1 #num1 = Player
			rot2 = self.object_inf[num2][3]
			if self.object_inf[num2][4] == 1:
				if rot2 % 180 == 0 :
					self.object_stop[num1] = (1,)
				if rot2 % 180 == 90 :
					self.object_stop[num1] = (2,)
			'''elif self.object_inf[num2][4] == 3:
				 self.object_inf[num1][] == 1'''
				
		if s == {'Player','Bonus'} :
			if self.object_inf[num1][0] == 'Bonus':
				num1, num2 = num2, num1 #num1 = Player
			self.object_stop[num1] = (3,self.object_inf[num2][1],self.object_inf[num2][2])
				
		if s == {'Pula','Stena'}:
			#num1 = Stena
			self.object_die_now.append(num2)
		
			
	def die_object (self,num):
		#print(num,'{}')
		self.object_die_number.append (num)
		self.do(Delay(0.001))
		self.object_inf[num] = ('None',0,0,0)
		self.object_inf_future[num] = ('None',0,0,0)
		self.object[num] = 'None'
class Player(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self,player,inf,color,number,rot=0):
		super().__init__()
		
		self.number = number
		self.player = player
		self.color = color
		self.rot = rot/180*pi
		self.player.position = (inf[1],inf[2])
		'''
		if color == 'red':
			self.rot = 0
		if color == 'blue':
			self.rot = pi
		'''
		self.player.rotation = (self.rot*(180/pi))
		
		self.v=4
		self.maxbomb=3
		self.timereload=3.5
		self.bomb = 3
		self.keys=set()
		#make player
		self.add(self.player)
		#Запускаем
		self.player.do(Repeat(Delay(0.001)+CallFunc(self.phizic)))
		
	def reload(self):
		self.bomb += 1
		if self.bomb < self.maxbomb :
			self.player.do(Delay(self.timereload)+CallFunc(self.reload))
	def on_key_release(self, keys, mod):
		self.keys.remove(keys)
	def on_key_press(self, keys, mod):
		# LEFT,a: выстрел
		# RIGTH,d: поворот
		self.keys.add(keys)
		
		#Pula
		if (key.LEFT in self.keys and self.color=='red')or (key.A in self.keys and self.color=='blue'):
			if self.bomb == self.maxbomb:
				self.player.do(Delay(self.timereload)+CallFunc(self.reload))
			if self.bomb > 0 :
				self.bomb -= 1
				x, y = self.player.position
				#Работа с выстрелом
				self.do(Delay(0.001))
				self.parent.v = self.v
				self.parent.rot = self.rot
				self.parent.all_build_object('Pula',x,y)
		
	def phizic(self):
		deltarot=0.1
		timerot=0.01
		x, y = self.player.position
		sign = self.parent.sign
		if (key.RIGHT in self.keys and self.color=='red') or (key.D in self.keys and self.color=='blue'):
			self.rot = self.rot + sign*deltarot
			
		Vx = self.v*sin(self.rot)
		Vy = self.v*cos(self.rot)
		stop = self.parent.object_stop[self.number]
		
		#print(stop,'-')
		if stop == (2,):
			y = y + Vy
		elif stop == (1,):
			x = x + Vx
		elif 3 in stop:
			x0 = stop[1] 
			y0 = stop[2] 
			if abs(x-x0) >= abs (y-y0):
				x, y = x, y+Vy
			elif abs(x-x0) < abs (y-y0):
				x, y = x + Vx, y 
			else: 
				x, y = x , y
		elif stop == (0,):
			x, y = x + Vx, y + Vy
			
		self.parent.object_stop[self.number] = (0,)
		#Выдача координат директору
		#print(self.number + self.parent.delta_number(self.number),'-')
		self.parent.object_inf_future[self.number]  = 'Player', x , y, self.rot
		
		'''#import pdb; pdb.set_trace()'''
		
		#Изменение координат и угла
		self.player.position = x, y
		self.player.rotation = (self.rot*(180/pi))
class Pula (cocos.layer.Layer):
	def __init__(self,pula,v,rot,inf,number):
		super().__init__()
		
		self.pula = pula
		self.number = number
		#Выдача скорости и поворота
		self.v0=v*2.5
		self.rot=rot
		#Вывод на экран
		self.pula.position= inf[1], inf[2]
		self.add(self.pula)
		#Начинаем полет
		self.pula.do(Repeat(Delay(0.001)+CallFunc(self.phizic)))
	def phizic (self):
		
		Vx = self.v0*sin(self.rot)
		Vy = self.v0*cos(self.rot)
		x, y = self.pula.position
		x, y = x + Vx, y + Vy
		
		#Проверка расположения+delta coordinat
		self.pula.position = x+Vx,y+Vy
		#Выдача координат директору
		self.parent.object_inf_future[self.number]  = 'Pula', x , y
		if self.number in self.parent.object_die_number:
			#print('-----------')
			self.remove(self.pula)
class Bonus (cocos.layer.Layer):
	def __init__(self,bonus, inf, number):
		super().__init__()
		self.number = number
		self.bonus = bonus
		self.inf = inf
		self.bonus.position = inf[1],inf[2]
		
		self.add(self.bonus)
		self.bonus.do(Repeat(Delay(0.001)+CallFunc(self.phizic)))
	def phizic (self):
		x, y = self.bonus.position
		if self.number in self.parent.object_die_number:
			self.remove(self.bonus)
			#Vibor vida
			vids = ['Revers']
			if self.inf[0] == 'Bonus':
				l=int(len (vids))
				num = randint(0,l-1)
				self.parent.all_build_object(vids[num],x,y)
			if self.inf[0] == 'Revers':
				self.parent.sign *= -1
class Stena (cocos.layer.Layer):
	def __init__(self,stena, inf, number,rot=0):
		super().__init__()
		self.number = number
		self.stena = stena
		self.inf = inf
		self.rot = rot
		self.stena.position = inf[1],inf[2]
		self.stena.rotation = rot
		self.add(self.stena)
		
		
		
cocos.director.director.init(width =size[0],height =size[1])
cocos.director.director.run(MainScene())
