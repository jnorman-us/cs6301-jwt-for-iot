import PySimpleGUI as sg

def page(error):
	layout = [
		[sg.Text('ERROR!')],
		[sg.Text(error)],
	]
	return sg.Window(title(), layout, finalize=True)

def title():
	return 'Error!'