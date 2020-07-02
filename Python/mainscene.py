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
