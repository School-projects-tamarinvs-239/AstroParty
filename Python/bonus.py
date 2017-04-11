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
			self.remove(sel f.bonus)
			#Vibor vida
			vids = ['Revers']
			if self.inf[0] == 'Bonus':
				l=int(len (vids))
				num = randint(0,l-1)
				self.parent.all_build_object(vids[num],x,y)
			if self.inf[0] == 'Revers':
				self.parent.sign *= -1