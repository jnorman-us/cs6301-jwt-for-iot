import time
import jwt as jsonWT

from Crypto.Hash import SHA256
from Crypto.Util import strxor
from Crypto.Random import get_random_bytes

import records

secret = 'this is the secret key'

class Server:
	def __init__(self):
		self.users = records.getUsers()
		self.devices = records.getDevices()

	def login(self, id, E, HPWclient):
		user = None
		for u in self.users:
			if u['id'] == id:
				user = u
				break

		if user == None:
			return False

		h = SHA256.new()
		h.update(str.encode(user['password']))
		HPW = h.digest()

		print('\nSERVER AUTHENTICATING USER')	
		if HPW != HPWclient:
			print('\tHashed Passwords did not match')
			return False, None, None

		I = strxor.strxor(HPW, E)
		R = get_random_bytes(32)
		secretKey = get_random_bytes(32)
		token = jsonWT.encode({
			"secretKey": secretKey.hex(),
		}, secret, algorithm="HS256")

		# save for later
		user['secretKey'] = secretKey
		user['I'] = I
		user['R'] = R

		print('\tHASHED-PASSWORD', HPW.hex())
		print('\tJWT', token)
		print('\tSecret-Key', secretKey.hex())
		print('\tI-user', I.hex())
		print('\tR-user', R.hex())
		print('\tLOGIN AUTHORIZED')
		return True, token, R

	def api(self, user_id, jwt, K, device_id, timestamp):
		user = None
		for u in self.users:
			if u['id'] == user_id:
				user = u
				break
		if user == None:
			return False

		print('\nSERVER AUTHORIZING CLIENT API CALL')
		Iclient = strxor.strxor(K, user['R'])
		print('\tI-calculated', Iclient.hex())
		print('\tI-expected  ', user['I'].hex())
		if Iclient != user['I']:
			print('\tI\'s do not match!')
			return False

		token = jsonWT.decode(jwt, secret, algorithms=["HS256"])
		print('\tSecret Key from JWT', token['secretKey'])
		print('\tSecret Key Expected', user['secretKey'].hex())
		if token['secretKey'] != user['secretKey'].hex():
			print('\tSecret keys do not match!')
			return False

		for d in self.devices:
			if d['id'] == device_id:
				d['on'] = not d['on']
				break
		print('\tDEVICE API CALL AUTHORIZED')
		return True

	def addDevice(self, Rdevice, client):
		print('\nSERVER ADDING DEVICE')
		TIMESTAMP = int(time.time()).to_bytes(32, 'big')
		Cdevice = strxor.strxor(client.random, Rdevice)
		print('\tTimestamp', TIMESTAMP.hex())
		print('\tC-device', Cdevice.hex())

		Emessage, Sclient = client.getDeviceApproval(Cdevice, TIMESTAMP)
		print('\nSERVER CHALLENGES DEVICE')
		Auser = strxor.strxor(Emessage, client.random)
		print('\tA-user', Auser.hex())

		print('\nDEVICE ANSWERING CHALLENGE')
		Adc = strxor.strxor(Auser, Rdevice)
		h = SHA256.new()
		h.update(Adc)
		HAdc = h.digest()
		Sdevice = strxor.strxor(HAdc, Rdevice)
		print('\tS-device', Sdevice.hex())

		print('\nSERVER REVIEWS IF S-client XOR Ruser == S-device XOR Rdevice')
		Xclient = strxor.strxor(Sclient, client.random)
		Xdevice = strxor.strxor(Sdevice, Rdevice)
		print('\tXOR client', Xclient.hex())
		print('\tXOR device', Xdevice.hex())
		if Xclient != Xdevice:
			print('\tCheck failed, device not added')
			return False
		print('\tCheck passed, adding new device')

		self.devices.append({
			'id': len(self.devices) + 1,
			'on': False,
			'R': Rdevice,
		})
		return True

