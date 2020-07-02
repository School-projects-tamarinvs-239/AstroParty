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