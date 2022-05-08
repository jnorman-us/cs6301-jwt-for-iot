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

		print('>>>>>SERVER CALCULATIONS')	
		if HPW != HPWclient:
			print('Hashed Passwords did not match')
			print('------------------------\n')
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

		print('HASHED PASSWORD', HPW.hex())
		print('JWT            ', token)
		print('Secret Key     ', secretKey.hex())
		print('I              ', I.hex())
		print('R              ', R.hex())
		print('LOGIN AUTHORIZED')
		print('------------------------\n')
		return True, token, R

	def api(self, user_id, jwt, K, device_id, timestamp):
		user = None
		for u in self.users:
			if u['id'] == user_id:
				user = u
				break
		if user == None:
			return False

		print('>>>>>SERVER CALCULATIONS')
		Iclient = strxor.strxor(K, user['R'])
		print('I calculated', Iclient.hex())
		print('I expected  ', user['I'].hex())
		if Iclient != user['I']:
			print('I\'s do not match!')
			return False

		token = jsonWT.decode(jwt, secret, algorithms=["HS256"])
		print('Secret Key from JWT', token['secretKey'])
		print('Secret Key Expected', user['secretKey'].hex())
		if token['secretKey'] != user['secretKey'].hex():
			print('Secret keys do not match!')
			return False

		for d in self.devices:
			if d['id'] == device_id:
				d['on'] = not d['on']
				break
		time.sleep(2)
		print('DEVICE API CALL AUTHORIZED')
		print('------------------------\n')
		return True
