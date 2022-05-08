from Crypto.Random import get_random_bytes

userRecords = [{
	'id': 'joseph',
	'password': 'test1234',
}, {
	'id': 'asd',
	'password': 'asd',
}, {
	'id': 'alex',
	'password': 'bruhasd',
}, {
	'id': 'robert',
	'password': 'ihop',
}, {
	'id': 'david',
	'password': 'lawrence',
}]

def getUsers():
	return userRecords

devices = [{
	'id': 1,
	'on': False,
	'R': get_random_bytes(32),
}, {
	'id': 2,
	'on': True,
	'R': get_random_bytes(32),
}, {
	'id': 3,
	'on': False,
	'R': get_random_bytes(32),
}, {
	'id': 4,
	'on': False,
	'R': get_random_bytes(32),
}]

def getDevices():
	return devices