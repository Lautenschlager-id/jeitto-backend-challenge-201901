import database as db
from decorators import cache, check_maintenance, remove_cache, require_access_token
from flask import request
from flask_restful import Resource
from utils import get_list_id, handle_invalid_parameter, HttpStatus, json_response

def format_products(data):
	"""Formats the products that are stored as ('index':value) to a more appropriate response format."""
	products = [ ]

	for (id, value) in data.items():
		products.append({
			"id": id,
			"value": value
		})

	return products

def is_valid_product(product, ignore_id = False):
	"""Checks whether a product dictionary is valid."""
	# A valid product has the values 'id'<string> and 'value'<number>
	return (ignore_id or isinstance(product.get("id"), str)) and (isinstance(product.get("value"), float) or isinstance(product.get("value"), int))

class Product(Resource):
	"""Represents the '/phone/product' endpoint and accepts GET, POST, PUT, and DELETE methods."""

	@check_maintenance("phone", "general")
	@require_access_token
	@cache("get_product")
	def get(self):
		"""GET /phone/product
			Retrieves all phone recharge products offered by registered companies.
			
			Query string:
				company_id (optional) - A filter to only list products from the given company.

			Statuses:
				200 - Success.
				400 - When given company_id is invalid.
				403 - Unauthorized access to the endpoint.
				503 - Maintenance mode, i.e., impossible to perform any action.

			Response example [JSON][200]:
				No filter:
				[
					{
						"company_id": "lilith",
						"products": [
							{
								"id": "lili_666",
								"value": 666.00
							}
						]
					}
				]

				With filter:
				{
					"company_id": "lilith",
					"products": [
						{
							"id": "lili_666",
							"value": 666.00
						}
					]
				}
		"""
		company_id = request.args.get("company_id")
		if (company_id):
			phone_recharge_products = list(db.phone_recharge_products.find({ "company_id": company_id }))
			if (len(phone_recharge_products) == 0):
				return handle_invalid_parameter("invalid_company", company_id, get_list_id(db.phone_recharge_products.find({ }), "company_id"), var = (company_id, "company_id"))

			# Displays data from specific company
			return json_response({
				"company_id": company_id,
				"products": format_products(phone_recharge_products[0]["products"])
			})
		else:
			response_message = [ ]

			for product in list(db.phone_recharge_products.find({ })):
				response_message.append({
					"company_id": product["company_id"],
					"products": format_products(product["products"])
				})

			# Displays data from all companies
			return json_response(response_message)

	@check_maintenance("phone", "general")
	@check_maintenance("phone", "product")
	@require_access_token
	@remove_cache("get_product")
	def post(self):
		"""POST /phone/product
			Inserts new phone recharge products that are offered by a company.
			
			Body [JSON]:
				company_id <string> - The ID of the company which offers the new products.
				products <list<dict>> - The list of products to be inserted.
					products.dict.id <string> - The product ID.
					products.dict.value <float> - The product price.

				Example:
				{
					"company_id": "lilith",
					"products": [
						{
							"id": "lili_666",
							"value": 666.00
						},
						{
							"id": "lili_69",
							"value": 69.00
						}
					]
				}

			Statuses:
				201 - Inserted with success.
				400 - When given company_id or products is invalid.
				400 - When no product gets inserted. (duplicates, bad indexes, etc)
				403 - Unauthorized access to the endpoint.
				503 - Maintenance mode, i.e., impossible to perform any action.

			Response example [JSON][201]:
				location <string> - The GET path to check the inserted items.
				ignored <list<dict>> - The list of products that got ignored. Products can get ignored when they already exist in the database or when they have an invalid format.

				Example:
				{
					"location": "/phone/product?company_id=lilith",
					"ignored": [
						{
							"id": "lili_666",
							"value": 666.00
						}
					] 
				}
		"""
		body = request.get_json(force = True)

		company_id = body.get("company_id")
		if (not isinstance(company_id, str)):
			return handle_invalid_parameter("invalid_value", "company_id")

		products = body.get("products")
		if (not isinstance(products, list)):
			return handle_invalid_parameter("invalid_value", "products")

		# Filter and Create
		is_new = False
		phone_recharge_products = list(db.phone_recharge_products.find({ "company_id": company_id }))
		if (len(phone_recharge_products) == 0):
			is_new = True
			phone_recharge_products.append({
				"company_id": company_id,
				"products": { }
			})
		phone_recharge_products = phone_recharge_products[0]

		ignored = [ ]
		for product in products:
			if ((product.get("id") is not None and product.get("value") is not None) and (not product["id"] in phone_recharge_products["products"]) and is_valid_product(product)):
				phone_recharge_products["products"][product["id"]] = product["value"]
			else:
				ignored.append(product)

		failed = (len(products) == len(ignored))
		if (not failed):
			if (is_new):
				db.phone_recharge_products.insert_one(phone_recharge_products)
			else:
				db.phone_recharge_products.replace_one({ "company_id": company_id }, phone_recharge_products)

		return json_response({
			"location": "/phone/product?company_id=" + company_id,
			"ignored": ignored
		}, (HttpStatus.BAD_REQUEST if failed else HttpStatus.CREATED))

	@check_maintenance("phone", "general")
	@check_maintenance("phone", "product")
	@require_access_token
	@remove_cache("get_product")
	def put(self):
		"""PUT /phone/product
			Edits phone recharge products that are offered by a company.
			
			Body [JSON]:
				company_id <string> - The ID of the company which offers the products.
				products <list<dict>> - The list of products to be edited.
					products.dict.id <string> - The product ID.
					products.dict.value <float> - The product price.

				Example (changes the value of lili_666 to 69.00):
				{
					"company_id": "lilith",
					"products": [
						{
							"id": "lili_666",
							"value": 69.00
						},
						{
							"id": "lili_05",
							"value": 1.00
						}
					]
				}

			Statuses:
				200 - Success.
				400 - When given company_id or products is invalid.
				400 - When no product gets edited. (invalid, bad indexes, etc)
				403 - Unauthorized access to the endpoint.
				503 - Maintenance mode, i.e., impossible to perform any action.

			Response example [JSON][200]:
				location <string> - The GET path to check the edited items.
				ignored <list<dict>> - The list of products that got ignored. Products can get ignored when they do not exist in the database or when they have an invalid format.

				Example:
				{
					"location": "/phone/product?company_id=lilith",
					"ignored": [
						{
							"id": "lili_05",
							"value": 1.00
						}
					] 
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

		products = body.get("products")
		if (not isinstance(products, list)):
			return handle_invalid_parameter("invalid_value", "products")

		# Filter and Edit
		ignored = [ ]
		for product in products:
			if ((product.get("value") is not None) and (product.get("id") in phone_recharge_products["products"]) and is_valid_product(product, True)):
				phone_recharge_products["products"][product["id"]] = product["value"]
			else:
				ignored.append(product)

		failed = (len(products) == len(ignored))
		if (not failed):
			db.phone_recharge_products.replace_one({ "company_id": company_id }, phone_recharge_products)

		return json_response({
			"location": "/phone/product?company_id=" + company_id,
			"ignored": ignored
		}, (HttpStatus.BAD_REQUEST if failed else HttpStatus.SUCCESS))

	@check_maintenance("phone", "general")
	@check_maintenance("phone", "product")
	@require_access_token
	@remove_cache("get_product")
	def delete(self):
		"""DELETE /phone/product
			Deletes phone recharge products that are offered by a company.
			If the company gets all its products deleted, it will also be deleted.

			Body [JSON]:
				company_id <string> - The ID of the company which offers the products.
				product_ids <list<string>> - The list of product IDs to be deleted.

				Example:
				{
					"company_id": "lilith",
					"product_ids": [ "lili_666", "lili_69", "lili_05" ]
				}

			Statuses:
				200 - Success.
				400 - When given company_id or product_ids is invalid.
				400 - When no product gets deleted. (invalid, etc)
				403 - Unauthorized access to the endpoint.
				503 - Maintenance mode, i.e., impossible to perform any action.

			Response example [JSON][200]:
				location <string> - The GET path to the company which the items were deleted of.
				ignored <list<dict>> - The list of products that got ignored. Products can get ignored when they do not exist in the database or when they have an invalid format.

				Example:
				{
					"location": "/phone/product?company_id=lilith",
					"ignored": [ "lili_05" ] 
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

		product_ids = body.get("product_ids")
		if (not isinstance(product_ids, list)):
			return handle_invalid_parameter("invalid_value", "product_ids")

		# Filter and Remove
		ignored = [ ]
		for id in product_ids:
			if (id in phone_recharge_products["products"]):
				del phone_recharge_products["products"][id]
			else:
				ignored.append(id)

		failed = (len(product_ids) == len(ignored))
		if (not failed):
			if (len(phone_recharge_products["products"]) == 0):
				db.phone_recharge_products.delete_one({ "company_id": company_id })
			else:
				db.phone_recharge_products.replace_one({ "company_id": company_id }, phone_recharge_products)

		return json_response({
			"location": "/phone/product?company_id=" + company_id,
			"ignored": ignored
		}, (HttpStatus.BAD_REQUEST if failed else HttpStatus.SUCCESS))