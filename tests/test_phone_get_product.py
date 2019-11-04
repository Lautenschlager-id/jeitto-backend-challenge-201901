import unittest
from tests.utils import *

data = [
	{ # Get all
		"code": 200,
		"query": '',
		"response": '[{"company_id": "tim", "products": [{"id": "tim_05", "value": 5.0}, {"id": "tim_08", "value": 8.0}, {"id": "tim_10", "value": 10.0}, {"id": "tim_15", "value": 15.0}, {"id": "tim_20", "value": 20.0}]}, {"company_id": "vivo", "products": [{"id": "vivo_05", "value": 5.0}, {"id": "vivo_10", "value": 10.0}, {"id": "vivo_15", "value": 15.0}, {"id": "vivo_20", "value": 20.0}, {"id": "vivo_50", "value": 50.0}]}, {"company_id": "claro", "products": [{"id": "claro_05", "value": 5.0}, {"id": "claro_10", "value": 10.0}]}, {"company_id": "oi", "products": [{"id": "oi_10", "value": 10.0}, {"id": "oi_30", "value": 30.0}]}]'
	},
	{ # Valid company_id
		"code": 200,
		"query": '?company_id=tim',
		"response": '{"company_id": "tim", "products": [{"id": "tim_05", "value": 5.0}, {"id": "tim_08", "value": 8.0}, {"id": "tim_10", "value": 10.0}, {"id": "tim_15", "value": 15.0}, {"id": "tim_20", "value": 20.0}]}'
	},
	{ # Invalid company_id
		"code": 400,
		"query": '?company_id=beelzebub',
		"response": '{"code": "0100", "message": "The company of ID \'beelzebub\' does not provide any phone recharging service. These are the available company IDs: \'tim\', \'vivo\', \'claro\', \'oi\'"}'
	}
]

class TestGetProduct(unittest.TestCase):
	def setUp(self):
		populate_company_data()

	def tearDown(self):
		pass

	def test_status(self):
		for t in data:
			self.assertEqual(http_request("GET", "phone/product" + t["query"]).status_code, t["code"])

	def test_get_response(self):
		for t in data:
			self.assertEqual(http_request("GET", "phone/product" + t["query"]).text, t["response"])