import json

def read_json_file(filename):
	"""Loads a JSON string from a file"""
	file = None
	try:
		with open(filename, 'r') as data:
			file = json.load(data)
	except:
		pass

	return file

ENV = read_json_file("ENV.json")
MSG = read_json_file("messages.json")

CACHE = { }