import traceback
import PySimpleGUI as sg

import pages.login as login
import pages.error as error
import pages.devices as devices

from client import Client
from server import Server

from records import getDevices

def main():
	sg.theme('HotDogStand')
	window = login.form()
	client = Client()
	server = Server()

	while True:
		event, values = window.read()
		if event in (None, 'Close'):
			break
		elif type(event) is tuple:
			command = event[0]
			try:
				if window.Title == login.title():
					if command == 'login':
						login.login(event, values, client, server)

						if client.loggedIn():
							window.close()
							window = devices.form(client, getDevices())
				if window.Title == devices.title():
					if command == 'toggle':
						devices.toggle(event, values, client, server)

						window.close()
						window = devices.form(client, getDevices())
					if command == 'add':
						devices.add(event, values, client, server)
						window.close()
						window = devices.form(client, getDevices())
			except Exception as e:
				traceback.print_exc()
				print(e)
				window.close()
				window = error.page(str(e))


	window.close()

if __name__ == '__main__':
	main()

