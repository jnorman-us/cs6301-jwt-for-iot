from Crypto.Hash import SHA256
from Crypto.Util import strxor
from Crypto.Random import get_random_bytes

class Client:
	def __init__(self):
		self.username = None
		self.I = None
		self.salt = None
		self.jwt = None
		self.random = None

	def loggedIn(self):
		return self.jwt != None

	def getDeviceApproval(self, C, timestamp):
		print('\nUSER APPROVING DEVICE')
		Rdevice = strxor.strxor(C, self.random)
		Adc = get_random_bytes(32)
		Auser = strxor.strxor(Adc, Rdevice)
		Emessage = strxor.strxor(Auser, self.random)

		print('\tR-device', Rdevice.hex())
		print('\tA-d-c', Adc.hex())
		print('\tA-user', Auser.hex())
		print('\tE-message', Emessage.hex())

		h = SHA256.new()
		h.update(Adc)
		HAdc = h.digest()
		Sclient = strxor.strxor(HAdc, self.random)

		print('\tS-client', Sclient.hex())

		return Emessage, Sclient
