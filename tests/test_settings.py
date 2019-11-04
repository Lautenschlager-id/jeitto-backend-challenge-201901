import database as db
import unittest
from tests.utils import *

def run_all(self, code, response, ignore_get = False, **kwargs):
	# Product
	for method in [ "get", "post", "put", "delete" ]:
		if (ignore_get): continue
		request = http_request(method, "phone/product", **kwargs)
		self.assertEqual(request.status_code, code)
		self.assertEqual(request.text, response)
	# Recharge
	for method in [ "get", "post" ]:
		if (ignore_get): continue
		request = http_request(method, "phone/recharge", **kwargs)
		self.assertEqual(request.status_code, code)
		self.assertEqual(request.text, response)

class TestSettings(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_unauthorized(self):
		run_all(self, 403, '{"code": "0001", "message": "Access denied. Missing a Access Token."}', headers = None)

	def test_maintenance(self):
		response = '{"code": "0000", "message": "This service is currently unavailable due to an ongoing maintenance. Try again later."}'

		# Set maintenance mode
		db.set_maintenance("phone", "recharge", True)
		db.set_maintenance("phone", "product", True)

		run_all(self, 503, response, ignore_get = True)

		# Set maintenance mode
		db.set_maintenance("phone", "recharge", False)
		db.set_maintenance("phone", "product", False)

		db.set_maintenance("phone", "general", True)
		run_all(self, 503, response)
		db.set_maintenance("phone", "general", False)