import database as db
import datetime
import re as regex
from decorators import cache, check_maintenance, remove_cache, require_access_token
from flask import request
from flask_restful import Resource
from utils import get_list_id, handle_invalid_parameter, HttpStatus, json_response

def query_filter(data, args):
	"""Performs a query filter into a given dictionary."""
	for (key, value) in data.items():
		if (key not in args): continue
		if (str(value) != args[key]):
			return False
	return True

class Recharge(Resource):
	"""Represents the '/phone/recharge' endpoint and accepts GET, and POST methods."""

	@check_maintenance("phone", "general")
	@require_access_token
	@cache("get_recharge")
	def get(self):
		"""GET /phone/recharge
			Retrieves all phone recharges transactioned by the users.
			The query string behaves like a filter and allows combinations.

			Query string:
				id (optional) - The transaction unique ID.
				company_id (optional) - Recharges related to the given company ID.
				product_id (optional) - Recharges related to the given product ID.
				phone_number (optional) - Recharges related to the given phone number.
				created_at (optional) - Recharges performed in a specific time. Uses the format "YearMonthDayTHourMinuteSecond.MillisecondZ", e.g.: "20191019T221015.00Z"

			Statuses:
				200 - Success.
				403 - Unauthorized access to the endpoint.
				503 - Maintenance mode, i.e., impossible to perform any action.

			Response example [JSON][200]:
				No filter:
				[
					{
						"id": 0,
						"created_at": "20191019T221015.00Z",
						"company_id": "lilith",
						"product_id": "lili_69",
						"phone_number": "11966669999",
						"value": 69.00 
					},
					{
						"id": 1,
						"created_at": "20191019T221015.00Z",
						"company_id": "lilith",
						"product_id": "lili_666",
						"phone_number": "11940028922",
						"value": 666.00 
					}
				]

				With filter 'product_id=lili_666':
				{
					"id": 1,
					"created_at": "20191019T221015.00Z",
					"company_id": "lilith",
					"product_id": "lili_666",
					"phone_number": "11940028922",
					"value": 666.00 
				}
		"""
		recharges = [ ]

		for recharge in db.phone_recharges.find({ }):
			del recharge["_id"] # bad mongo
			if (query_filter(recharge, request.args)):
				recharges.append(recharge)

		return json_response(recharges)

	@check_maintenance("phone", "general")
	@check_maintenance("phone", "recharge")
	@require_access_token
	@remove_cache("get_recharge")
	def post(self):
		"""POST /phone/recharge
			Performs and registers a new phone recharge transaction.
			
			Body [JSON]:
				company_id <string> - The ID of the company which offers the product.
				product_id <string> - The product being purchased.
				phone_number <string> - The phone number which is receiving the phone recharge. Its format gets handled.

				Example:
				{
					"company_id": "lilith",
					"product_id": "lili_666",
					"phone_number": "(11)94002-8922"
				}

			Statuses:
				201 - Transaction completed with success.
				400 - When given company_id or product_id is invalid.
				400 - When no product is found. (invalid, etc)
				403 - Unauthorized access to the endpoint.
				503 - Maintenance mode, i.e., impossible to perform any action.

			Response example [JSON][201]:
				id <int> - The transaction ID.
				created_at <string> - The timestamp related to the transaction. Uses the format "YearMonthDayTHourMinuteSecond.MillisecondZ", e.g.: "20191019T221015.00Z"
				company_id <string> - The ID of the company attached to the product purchased.
				product_id <string> - The ID of the product purchased.
				phone_number <string> - The phone number that received the phone recharge.
				value <float> - The product price.

				Example:
				{
					"id": 1,
					"created_at": "20191019T221015.00Z",
					"company_id": "lilith",
					"product_id": "lili_666",
					"phone_number": "11940028922",
					"value": 666.00 
				}
		"""
		body = request.get_json(force = True)

		company_id = body.get("company_id")
		if (not isinstance(company_id, str)):
			company_id = None # Joins the next if

		phone_recharge_products = list(db.phone_recharge_products.find({ "company_id": company_id }))
		if (len(phone_recharge_products) == 0):
			return handle_invalid_parameter("invalid_company", company_id, get_list_id(db.phone_recharge_products.find({ }), "company_id"), var = (company_id, "company_id"))
		phone_recharge_products = phone_recharge_products[0]

		product_id = body.get("product_id")
		if (not isinstance(product_id, str)):
			product_id = None # Joins the next if
		if (product_id not in phone_recharge_products["products"]):
			return handle_invalid_parameter("invalid_company_recharge", product_id, company_id, get_list_id(phone_recharge_products["products"].keys(), ignore_filter = True), var = (product_id, "product_id"))

		phone_number_raw = body.get("phone_number")
		if (not isinstance(phone_number_raw, str)):
			return handle_invalid_parameter("invalid_value", "phone_number")

		phone_number = regex.match(r"^\(?0?(\d{2})\)? *(9) *(\d{4}) *-? *(\d{4})$", phone_number_raw)
		if (phone_number is None):
			return handle_invalid_parameter("invalid_phone_number", phone_number_raw, var = (phone_number_raw, "phone_number"))
		phone_number = ''.join(phone_number.groups())

		# Perform recharge
		recharge = {
			"id": db.count(db.phone_recharges),
			"created_at": datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ"),
			"company_id": company_id,
			"product_id": product_id,
			"phone_number": phone_number,
			"value": phone_recharge_products["products"][product_id]
		}

		db.phone_recharges.insert_one(recharge)
		del recharge["_id"]
		return json_response(recharge, HttpStatus.CREATED)