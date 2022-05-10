import PySimpleGUI as sg

from Crypto.Hash import SHA256
from Crypto.Util import strxor
from Crypto.Random import get_random_bytes

size = (20, 1)
def form():
	layout = [
		[sg.Text('Login to the IOT Home')],
		[sg.Text('Username'), sg.InputText(key='username')],
		[sg.Text('Password'), sg.InputText(key='password')],
		[sg.Button('Login', key=('login', None))],
	]
	return sg.Window(title(), layout, finalize=True)

def title():
	return 'JWT/IOT - Login'

def login(event, values, client, server):
	username = values['username']
	client.username = username
	password = values['password']

	salt = get_random_bytes(32)
	client.salt = salt

	h = SHA256.new()
	h.update(str.encode(username) + salt)
	I = h.digest()
	client.I = I

	h = SHA256.new()
	h.update(str.encode(password))
	HPW = h.digest()

	E = strxor.strxor(I, HPW)

	print('\nCLIENT LOGGING IN')
	print('\tI-user', I.hex())
	print('\tHashed-Password', HPW.hex())
	print('\tE-k', E.hex())

	success, jwt, random = server.login(username, E, HPW)

	client.jwt = jwt
	client.random = random
