import unittest
from tests.utils import *

data = [
	{ # Valid insertion
		"code": 201,
		"data": {"company_id": "nextel", "products": [{"id": "nextel_05", "value": 5.00}]},
		"response": '{"location": "/phone/product?company_id=nextel", "ignored": []}'
	},
	{ # Invalid company_id
		"code": 400,
		"data": {"company_id": 666},
		"response": '{"code": "0002", "message": "The value \'company_id\' has a bad type."}'
	},
	{ # Invalid products
		"code": 400,
		"data": {"company_id": "nextel", "products": 666},
		"response": '{"code": "0002", "message": "The value \'products\' has a bad type."}'
	},
	{ # Duplicate
		"code": 400,
		"data": {"company_id": "tim", "products": [{"id": "tim_05", "value": 5.0}]},
		"response": '{"location": "/phone/product?company_id=tim", "ignored": [{"id": "tim_05", "value": 5.0}]}'
	},
	{ # len(ignored) == len(products)
		"code": 400,
		"data": {"company_id": "nextel", "products": [{"id": "nextel_05", "value": "abaddon"}]},
		"response": '{"location": "/phone/product?company_id=nextel", "ignored": [{"id": "nextel_05", "value": "abaddon"}]}'
	},
	{ # len(ignored) < len(products)
		"code": 201,
		"data": {"company_id": "nextel", "products": [{"id": "nextel_05", "value": "abaddon"},{"id": "nextel_15", "value": 15.00}]},
		"response": '{"location": "/phone/product?company_id=nextel", "ignored": [{"id": "nextel_05", "value": "abaddon"}]}'
	}
]

class TestPostProduct(unittest.TestCase):
	def setUp(self):
		populate_company_data()

	def tearDown(self):
		pass

	def test_status(self):
		# No body
		self.assertEqual(http_request("POST", "phone/product").status_code, 400)

		# Body
		for t in data:
			self.assertEqual(http_request("POST", "phone/product", data = t["data"]).status_code, t["code"])

	def test_post_response(self):
		# No body
		response = '{"message": "The browser (or proxy) sent a request that this server could not understand."}\n'
		self.assertEqual(http_request("POST", "phone/product").text, response)

		# Body
		for t in data:
			self.assertEqual(http_request("POST", "phone/product", data = t["data"]).text, t["response"])