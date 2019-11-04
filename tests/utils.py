import database as db
from meta import ENV
import json, requests

def populate_company_data():
	# Restart
	db.phone_recharge_products.drop()
	db.populate_phone_recharge_products()

def populate_recharges_data():
	# Restart
	db.phone_recharges.drop()
	db.populate_phone_recharges()

url = "http://" + ENV["api"]["host"] + ":" + str(ENV["api"]["port"]) + "/"
header = { "authorization": db.access_token.aggregate([ { "$sample": { "size": 1 } } ]).next()["token"] } # Gets a random token
def http_request(method, path, headers = header, data = None):
	if (data is not None):
		data = json.dumps(data)
	return requests.request(method, url + path, headers = headers, data = data)