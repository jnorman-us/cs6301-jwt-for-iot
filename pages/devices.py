import time
import PySimpleGUI as sg

from Crypto.Util import strxor
from Crypto.Random import get_random_bytes

def form(client, devices):
	device_columns = []
	device_columns.append([
		sg.Text('ID', size=(3, 1)),
		sg.Text('State', size=(10, 1)),
		sg.Text('Toggle', size=(10, 1)),
	])

	for device in devices:
		device_columns.append([
			sg.Text(device['id'], size=(3, 1)),
			sg.Text('ON' if device['on'] else 'OFF', size=(10, 1)),
			sg.Button('Toggle', key=('toggle', device['id'])),
		])

	layout = [
		[sg.Text('Device List')],
		[
			sg.Text('JWT'), 
			sg.InputText(disabled=True, default_text=client.jwt, size=(60, 1))
		],
		[
			sg.Text('Random'), 
			sg.InputText(disabled=True, default_text=client.random.hex(), size=(60, 1))
		],
		[sg.Column(
			device_columns,
		)],
		[sg.Button('Add Device', key=('add', None))]
	]
	return sg.Window(title(), layout, finalize=True)

def title():
	return 'JWT/IOT - Devices'

def toggle(event, values, client, server):
	device_id = event[1]

	I = client.I
	K = strxor.strxor(client.I, client.random)
	TIMESTAMP = int(time.time()).to_bytes(4, 'big')

	print('\nCLIENT CALLS API TO SWITCH LIGHT')
	print('\tI-user', I.hex())
	print('\tK-user', K.hex())
	print('\tTimestamp', TIMESTAMP.hex())

	success = server.api(client.username, client.jwt, K, device_id, TIMESTAMP)

	if not success:
		raise Exception('Server call failed!')

def add(event, values, client, server):
	print('\nDEVICE BEING ADDED')
	Rdevice = get_random_bytes(32)
	print('\tR-device:', Rdevice.hex())

	server.addDevice(Rdevice, client)

