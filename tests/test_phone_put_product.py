import unittest
from tests.utils import *

data = [
	{ # Valid edition
		"code": 200,
		"data": {"company_id": "vivo", "products": [{"id": "vivo_05", "value": 7.00}]},
		"response": '{"location": "/phone/product?company_id=vivo", "ignored": []}'
	},
	{ # Invalid company_id
		"code": 400,
		"data": {"company_id": 666},
		"response": '{"code": "0002", "message": "The value \'company_id\' has a bad type."}'
	},
	{ # Invalid company_id
		"code": 400,
		"data": {"company_id": "nextel"},
		"response": '{"code": "0100", "message": "The company of ID \'nextel\' does not provide any phone recharging service. These are the available company IDs: \'tim\', \'vivo\', \'claro\', \'oi\'"}'
	},
	{ # Invalid products
		"code": 400,
		"data": {"company_id": "vivo", "products": 666},
		"response": '{"code": "0002", "message": "The value \'products\' has a bad type."}'
	},
	{ # len(ignored) == len(products)
		"code": 400,
		"data": {"company_id": "vivo", "products": [{"id": "vivo_55", "value": 55.00}]},
		"response": '{"location": "/phone/product?company_id=vivo", "ignored": [{"id": "vivo_55", "value": 55.0}]}'
	},
	{ # len(ignored) < len(products)
		"code": 200,
		"data": {"company_id": "vivo", "products": [{"id": "vivo_55", "value": 55.00},{"id": "vivo_05", "value": 55.00}]},
		"response": '{"location": "/phone/product?company_id=vivo", "ignored": [{"id": "vivo_55", "value": 55.0}]}'
	}
]

class TestPutProduct(unittest.TestCase):
	def setUp(self):
		populate_company_data()

	def tearDown(self):
		pass

	def test_status(self):
		# No body
		self.assertEqual(http_request("PUT", "phone/product").status_code, 400)

		# Body
		for t in data:
			self.assertEqual(http_request("PUT", "phone/product", data = t["data"]).status_code, t["code"])

	def test_put_response(self):
		# No body
		response = '{"message": "The browser (or proxy) sent a request that this server could not understand."}\n'
		self.assertEqual(http_request("PUT", "phone/product").text, response)

		# Body
		for t in data:
			self.assertEqual(http_request("PUT", "phone/product", data = t["data"]).text, t["response"])