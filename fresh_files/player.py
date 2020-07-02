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