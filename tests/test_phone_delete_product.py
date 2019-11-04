import unittest
from tests.utils import *

data = [
	{ # Valid deletion
		"code": 200,
		"data": {"company_id": "oi", "product_ids": ["oi_30"]},
		"response": '{"location": "/phone/product?company_id=oi", "ignored": []}'
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
	{ # Invalid product_ids
		"code": 400,
		"data": {"company_id": "oi", "product_ids": 666},
		"response": '{"code": "0002", "message": "The value \'product_ids\' has a bad type."}'
	},
	{ # len(ignored) == len(products)
		"code": 400,
		"data": {"company_id": "oi", "product_ids": ["oi_55"]},
		"response": '{"location": "/phone/product?company_id=oi", "ignored": ["oi_55"]}'
	},
	{ # len(ignored) < len(products)
		"code": 200,
		"data": {"company_id": "oi", "product_ids": ["oi_55", "oi_10"]},
		"response": '{"location": "/phone/product?company_id=oi", "ignored": ["oi_55"]}'
	}
]

class TestDeleteProduct(unittest.TestCase):
	def setUp(self):
		populate_company_data()

	def tearDown(self):
		pass

	def test_status(self):
		# No body
		self.assertEqual(http_request("DELETE", "phone/product").status_code, 400)

		# Body
		for t in data:
			self.assertEqual(http_request("DELETE", "phone/product", data = t["data"]).status_code, t["code"])

	def test_put_response(self):
		# No body
		response = '{"message": "The browser (or proxy) sent a request that this server could not understand."}\n'
		self.assertEqual(http_request("DELETE", "phone/product").text, response)

		# Body
		for t in data:
			self.assertEqual(http_request("DELETE", "phone/product", data = t["data"]).text, t["response"])
