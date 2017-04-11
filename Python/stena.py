	def __init__(self,stena, inf, number,rot=0):
		super().__init__()
		self.number = number
		self.stena = stena
		self.inf = inf
		self.rot = rot
		self.stena.position = inf[1],inf[2]
		self.stena.rotation = rot
		self.add(self.stena)