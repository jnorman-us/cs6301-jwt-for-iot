class Client:
	def __init__(self):
		self.username = None
		self.I = None
		self.salt = None
		self.jwt = None
		self.random = None

	def loggedIn(self):
		return self.jwt != None