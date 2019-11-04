# Product

## GET /phone/product
Retrieves all phone recharge products offered by registered companies.

| Query string | Required | Description                                            |
| :-:          | :-:      | -                                                      |
| company_id   | ✕        | A filter to only list products from the given company. |

| Response codes | Description                                               |
| :-:            | -                                                         |
| 200            | Success.                                                  |
| 400            | When given company_id is invalid.                         |
| 403            | Unauthorized access to the endpoint.                      |
| 503            | Maintenance mode, i.e., impossible to perform any action. |

#### Response example \[**JSON**\]\[**200**\]:
- No filter:
```JSON
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
```
- With filter:
```JSON
{
	"company_id": "lilith",
	"products": [
		{
			"id": "lili_666",
			"value": 666.00
		}
	]
}
```

## POST /phone/product
Inserts new phone recharge products that are offered by a company.

#### Body [**JSON**]:
- company_id \<string\> - The ID of the company which offers the new products.
- products \<list\<dict\>\> - The list of products to be inserted.
	- products.dict.id \<string\> - The product ID.
	- products.dict.value \<float\> - The product price.

##### Example
```JSON
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
```

| Response codes | Description                                                   |
| :-:            | -                                                             |
| 201            | Inserted with success.                                        |
| 400            | When given company_id or products is invalid.                 |
| 400            | When no product gets inserted. (duplicates, bad indexes, etc) |
| 403            | Unauthorized access to the endpoint.                          |
| 503            | Maintenance mode, i.e., impossible to perform any action.     |

#### Response example [**JSON**][**201**]:
- location \<string\> - The GET path to check the inserted items.
- ignored \<list<dict>\> - The list of products that got ignored. Products can get ignored when they already exist in the database or when they have an invalid format.

##### Example
```JSON
{
	"location": "/phone/product?company_id=lilith",
	"ignored": [
		{
			"id": "lili_666",
			"value": 666.00
		}
	] 
}
```

## PUT /phone/product
Edits phone recharge products that are offered by a company.

#### Body [**JSON**]:
- company_id \<string\> - The ID of the company which offers the products.
- products \<list\<dict\>\> - The list of products to be edited.
	- products.dict.id \<string\> - The product ID.
	- products.dict.value \<float\> - The product price.

##### Example
###### changes the value of lili_666 to 69.00
```JSON
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
```

| Response codes | Description                                                   |
| :-:            | -                                                             |
| 200            | Success.                                                      |
| 400            | When given company_id or products is invalid.                 |
| 400            | When no product gets edited. (invalid, bad indexes, etc)      |
| 403            | Unauthorized access to the endpoint.                          |
| 503            | Maintenance mode, i.e., impossible to perform any action.     |

#### Response example [**JSON**][**200**]:
- location \<string\> - The GET path to check the edited items.
- ignored \<list<dict>\> - The list of products that got ignored. Products can get ignored when they do not exist in the database or when they have an invalid format.

##### Example
```JSON
{
	"location": "/phone/product?company_id=lilith",
	"ignored": [
		{
			"id": "lili_05",
			"value": 1.00
		}
	] 
}
```

## DELETE /phone/product
Deletes phone recharge products that are offered by a company.<br>
If the company gets all its products deleted, it will also be deleted.

#### Body [**JSON**]:
- company_id \<string\> - The ID of the company which offers the products.
- product_ids \<list\<string\>\> - The list of product IDs to be deleted.

##### Example
```JSON
{
	"company_id": "lilith",
	"product_ids": [ "lili_666", "lili_69", "lili_05" ]
}
```

| Response codes | Description                                                   |
| :-:            | -                                                             |
| 200            | Success.                                                      |
| 400            | When given company_id or product_ids is invalid.              |
| 400            | When no product gets deleted. (invalid, etc)                  |
| 403            | Unauthorized access to the endpoint.                          |
| 503            | Maintenance mode, i.e., impossible to perform any action.     |

#### Response example [**JSON**][**200**]:
- location \<string\> - The GET path to the company which the items were deleted of.
- ignored \<list\<dict\>\> - The list of products that got ignored. Products can get ignored when they do not exist in the database or when they have an invalid format.

##### Example
```JSON
{
	"location": "/phone/product?company_id=lilith",
	"ignored": [ "lili_05" ] 
}
```

# Recharge

## GET /phone/recharge
Retrieves all phone recharges transactioned by the users.<br>
The query string behaves like a filter and allows combinations.

| Query string | Required | Description                                                                                                                          |
| :-:          | :-:      | -                                                                                                                                    |
| id           | ✕        | The transaction unique ID.                                                                                                           |
| company_id   | ✕        | Recharges related to the given company ID.                                                                                           |
| product_id   | ✕        | Recharges related to the given product ID.                                                                                           |
| phone_number | ✕        | Recharges related to the given phone number.                                                                                         |
| created_at   | ✕        | Recharges performed in a specific time.<br>Uses the format "YearMonthDayTHourMinuteSecond.MillisecondZ", e.g.: "20191019T221015.00Z" |

| Response codes | Description                                               |
| :-:            | -                                                         |
| 200            | Success.                                                  |
| 403            | Unauthorized access to the endpoint.                      |
| 503            | Maintenance mode, i.e., impossible to perform any action. |

#### Response example \[**JSON**\]\[**200**\]:
- No filter:
```JSON
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
```
- With filter `'product_id=lili_666'`:
```JSON
{
	"id": 1,
	"created_at": "20191019T221015.00Z",
	"company_id": "lilith",
	"product_id": "lili_666",
	"phone_number": "11940028922",
	"value": 666.00 
}
```

## POST /phone/recharge
Performs and registers a new phone recharge transaction.

#### Body [**JSON**]:
- company_id \<string\> - The ID of the company which offers the product.
- product_id \<string\> - The product being purchased.
- phone_number \<string\> - The phone number which is receiving the phone recharge. Its format gets handled.

##### Example
```JSON
{
	"company_id": "lilith",
	"product_id": "lili_666",
	"phone_number": "(11)94002-8922"
}
```

| Response codes | Description                                                   |
| :-:            | -                                                             |
| 201            | Transaction completed with success.                           |
| 400            | When given company_id or product_id is invalid.               |
| 400            | When no product is found. (invalid, etc)                      |
| 403            | Unauthorized access to the endpoint.                          |
| 503            | Maintenance mode, i.e., impossible to perform any action.     |

#### Response example \[**JSON**\]\[**200**\]:
- id \<int\> - The transaction ID.
- created_at \<string\> - The timestamp related to the transaction. Uses the format "YearMonthDayTHourMinuteSecond.MillisecondZ", e.g.: "20191019T221015.00Z"
- company_id \<string\> - The ID of the company attached to the product purchased.
- product_id \<string\> - The ID of the product purchased.
- phone_number \<string\> - The phone number that received the phone recharge.
- value \<float\> - The product price.

##### Example
```JSON
{
	"id": 1,
	"created_at": "20191019T221015.00Z",
	"company_id": "lilith",
	"product_id": "lili_666",
	"phone_number": "11940028922",
	"value": 666.00 
}
```