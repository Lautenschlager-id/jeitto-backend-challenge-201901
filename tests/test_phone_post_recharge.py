import json, unittest
from tests.utils import *

data = [
	{ # Valid insertion
		"code": 201,
		"data": {"company_id": "tim", "product_id": "tim_10", "phone_number": "(011)940028922"},
		"response": '{"id": 4, "created_at": "20191104T050214.511381Z", "company_id": "tim", "product_id": "tim_10", "phone_number": "11940028922", "value": 10.0}'
	},
	{ # Invalid company_id
		"code": 400,
		"data": {"company_id": 666},
		"response": '{"code": "0002", "message": "The value \'company_id\' has a bad type."}'
	},
	{ # Invalid company_id
		"code": 400,
		"data": {"company_id": "abraxas", "product_id": "tim_10", "phone_number": "(011)940028922"},
		"response": '{"code": "0100", "message": "The company of ID \'abraxas\' does not provide any phone recharging service. These are the available company IDs: \'tim\', \'vivo\', \'claro\', \'oi\'"}'
	},
	{ # Invalid product_id
		"code": 400,
		"data": {"company_id": "tim", "product_id": 666},
		"response": '{"code": "0002", "message": "The value \'product_id\' has a bad type."}'
	},
	{ # Invalid product_id
		"code": 400,
		"data": {"company_id": "tim", "product_id": "tim_40"},
		"response": '{"code": "0101", "message": "The recharge of ID \'tim_40\' has not been found in the services provided by the company of ID \'tim\'. These are the available recharge IDs for the specified company: \'tim_05\', \'tim_08\', \'tim_10\', \'tim_15\', \'tim_20\'"}'
	},
	{ # Invalid phone_number
		"code": 400,
		"data": {"company_id": "tim", "product_id": "tim_10", "phone_number": 696969},
		"response": '{"code": "0002", "message": "The value \'phone_number\' has a bad type."}'
	},
	{ # Invalid phone_number
		"code": 400,
		"data": {"company_id": "tim", "product_id": "tim_10", "phone_number": "119696969"},
		"response": '{"code": "0102", "message": "The phone number \'119696969\' is invalid."}'
	},
	{ # Formated phone_number
		"code": 201,
		"data": {"company_id": "tim", "product_id": "tim_10", "phone_number": "(011) 9 4002-8922"},
		"response": '{"id": 5, "created_at": "20191104T051219.689995Z", "company_id": "tim", "product_id": "tim_10", "phone_number": "11940028922", "value": 10.0}'
	}
]

class TestPostRecharge(unittest.TestCase):
	def setUp(self):
		populate_company_data()
		populate_recharges_data()

	def tearDown(self):
		pass

	def test_status(self):
		# No body
		self.assertEqual(http_request("POST", "phone/product").status_code, 400)

		# Body
		for t in data:
			self.assertEqual(http_request("POST", "phone/recharge", data = t["data"]).status_code, t["code"])

	def test_post_response(self):
		# No body
		response = '{"message": "The browser (or proxy) sent a request that this server could not understand."}\n'
		self.assertEqual(http_request("POST", "phone/recharge").text, response)

		# Body
		for t in data:
			# hack + a shame. Sorry;
			response = http_request("POST", "phone/recharge", data = t["data"])
			if (response.status_code == 201):
				t["response"] = json.loads(t["response"])
				t["response"]["created_at"] = json.loads(response.text)["created_at"]
				t["response"] = json.dumps(t["response"])

			self.assertEqual(response.text, t["response"])