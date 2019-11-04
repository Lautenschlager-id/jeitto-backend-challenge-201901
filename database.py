from meta import ENV
from pymongo import MongoClient

client                  = MongoClient(ENV["mongodb"]["host"], ENV["mongodb"]["port"])
client                  = client["jeitto_challenge"]

access_token            = client["access_token"]
phone_recharges         = client["phone_recharges"]
phone_recharge_products = client["phone_recharge_products"]
settings                = client["settings"]

def count(collection, filter = { }):
	"""Counts the number of registers in a query."""
	return collection.count_documents(filter)

def is_empty(collection):
	"""Checks whether the collection is empty."""
	return count(collection) == 0

def populate_access_token():
	"""Populates the 'access_token' collection."""
	access_token.insert_many([
		{ "token": "ybZMQFJWy7nik5R0ZqnAu1An9kfqPjn42WCRfEg2Ijo=" }, # Amon
		{ "token": "hMAAzkAygMqsAriWZ+pB1aZ9kdI2E42KQmB4BS7/iwk=" }, # Abaddon
		{ "token": "DVAFHQmcupOJIeygmTbCh+q2x3MI5LKochgJvoD2H1A=" }, # Abezethibou
		{ "token": "crWSSQ2zGAefAKBSEsCvkELdf53Xk7jvgQ2fRyu5yzs=" }, # Abraxas
		{ "token": "sCktAGZFqHrUIP4GDWnvqq7D+aSflXPPULPrLkydnts=" }, # Abyzou
		{ "token": "rL0etvLVdJYPEwuoWyFpnbxKpw0MntfjP+luTalCadY=" }  # Adrammelech
	])
if (is_empty(access_token)): populate_access_token()

def populate_settings():
	"""Populates the 'settings' collection."""
	settings.insert_one({
		"name": "phone_maintenance",
		"status": {
			"general": 0,
			"product": 0,
			"recharge": 0
		}
	})
if (is_empty(settings)): populate_settings()

def populate_phone_recharge_products():
	"""Populates the 'phone_recharge_products' collection."""
	phone_recharge_products.insert_one({
		"company_id": "tim",
		"products": {
			"tim_05": 5.00,
			"tim_08": 8.00,
			"tim_10": 10.00,
			"tim_15": 15.00,
			"tim_20": 20.00
		}
	})

	phone_recharge_products.insert_one({
		"company_id": "vivo",
		"products": {
			"vivo_05": 5.00,
			"vivo_10": 10.00,
			"vivo_15": 15.00,
			"vivo_20": 20.00,
			"vivo_50": 50.00
		}
	})

	phone_recharge_products.insert_one({
		"company_id": "claro",
		"products": {
			"claro_05": 5.00,
			"claro_10": 10.00
		}
	})

	phone_recharge_products.insert_one({
		"company_id": "oi",
		"products": {
			"oi_10": 10.00,
			"oi_30": 30.00
		}
	})
if (ENV["api"]["test"] and is_empty(phone_recharge_products)): populate_phone_recharge_products()

def populate_phone_recharges():
	"""Populates the 'phone_recharges' collection."""
	phone_recharges.insert_many([
		{
			"id": 0,
			"created_at": "20191019T221015.00Z",
			"company_id": "claro",
			"product_id": "claro_10",
			"phone_number": "11940028922",
			"value": 10
		},
		{
			"id": 1,
			"created_at": "20191019T221015.00Z",
			"company_id": "oi",
			"product_id": "oi_30",
			"phone_number": "11940028922",
			"value": 30
		},
		{
			"id": 2,
			"created_at": "20181019T221015.00Z",
			"company_id": "tim",
			"product_id": "tim_05",
			"phone_number": "19983400808",
			"value": 5
		},
		{
			"id": 3,
			"created_at": "20181019T221015.00Z",
			"company_id": "vivo",
			"product_id": "vivo_10",
			"phone_number": "19983400808",
			"value": 10
		}
	])
if (ENV["api"]["test"] and is_empty(phone_recharges)): populate_phone_recharges()

def get_maintenance_module(module):
	"""Gets a module that has maintenance flexibility in the settings."""
	module = list(settings.find({ "name": module + "_maintenance" }))

	if (len(module) == 0):
		return False
	return module[0]

def in_maintenance(module, service):
	"""Checks whether a specific service of a module is in maintenance."""
	module = get_maintenance_module(module)
	return module and (service in module["status"] and module["status"][service] == 1)

def set_maintenance(module, service, status = True):
	"""Sets the maintenance status to a specific service of a module."""
	_module = get_maintenance_module(module)
	if (not _module): return

	set = { "$set": { } }
	set["$set"]["status." + service] = (1 if status else 0)
	settings.update_one({ "name": module + "_maintenance" }, set)