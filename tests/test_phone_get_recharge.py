import unittest
from tests.utils import *

data = [
	{ # Get all
		"code": 200,
		"query": '',
		"response": '[{"id": 0, "created_at": "20191019T221015.00Z", "company_id": "claro", "product_id": "claro_10", "phone_number": "11940028922", "value": 10}, {"id": 1, "created_at": "20191019T221015.00Z", "company_id": "oi", "product_id": "oi_30", "phone_number": "11940028922", "value": 30}, {"id": 2, "created_at": "20181019T221015.00Z", "company_id": "tim", "product_id": "tim_05", "phone_number": "19983400808", "value": 5}, {"id": 3, "created_at": "20181019T221015.00Z", "company_id": "vivo", "product_id": "vivo_10", "phone_number": "19983400808", "value": 10}]'
	},
	{ # Get with search
		"code": 200,
		"query": "?id=1",
		"response": '[{"id": 1, "created_at": "20191019T221015.00Z", "company_id": "oi", "product_id": "oi_30", "phone_number": "11940028922", "value": 30}]'
	},
	{ # Get with search
		"code": 200,
		"query": "?company_id=vivo",
		"response": '[{"id": 3, "created_at": "20181019T221015.00Z", "company_id": "vivo", "product_id": "vivo_10", "phone_number": "19983400808", "value": 10}]'
	},
	{ # Get with search
		"code": 200,
		"query": "?product_id=oi_30",
		"response": '[{"id": 1, "created_at": "20191019T221015.00Z", "company_id": "oi", "product_id": "oi_30", "phone_number": "11940028922", "value": 30}]'
	},
	{ # Get with search
		"code": 200,
		"query": "?phone_number=11940028922",
		"response": '[{"id": 0, "created_at": "20191019T221015.00Z", "company_id": "claro", "product_id": "claro_10", "phone_number": "11940028922", "value": 10}, {"id": 1, "created_at": "20191019T221015.00Z", "company_id": "oi", "product_id": "oi_30", "phone_number": "11940028922", "value": 30}]'
	},
	{ # Get with search
		"code": 200,
		"query": "?phone_number=11940028922&company_id=claro",
		"response": '[{"id": 0, "created_at": "20191019T221015.00Z", "company_id": "claro", "product_id": "claro_10", "phone_number": "11940028922", "value": 10}]'
	}
]

class TestGetRecharge(unittest.TestCase):
	def setUp(self):
		populate_company_data()
		populate_recharges_data()

	def tearDown(self):
		pass

	def test_status(self):
		for t in data:
			self.assertEqual(http_request("GET", "phone/recharge" + t["query"]).status_code, t["code"])

	def test_get_response(self):
		for t in data:
			self.assertEqual(http_request("GET", "phone/recharge" + t["query"]).text, t["response"])