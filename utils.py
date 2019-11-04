import enum, json
from flask import Response
from meta import MSG

class HttpStatus(enum.Enum):
	"""Represents http status codes."""
	SUCCESS                = 200
	CREATED                = 201
	BAD_REQUEST            = 400
	UNAUTHORIZED           = 403
	NOT_FOUND              = 404
	CONFLICT               = 409
	SERVICE_UNAVAILABLE    = 503

class json_response(Response):
	"""An alias for the Response object to make json responses more readable."""
	def __init__(self, content = [], status = HttpStatus.SUCCESS):
		return super().__init__(
			json.dumps(content),
			status = (status.value if status in HttpStatus else status),
			mimetype = "application/json"
		)

def handle_invalid_parameter(message_id, *format, status = HttpStatus.BAD_REQUEST, var = (None, None)):
	"""Handles invalid parameters by sending an error response message.
	If @var is given, an invalid parameter message is thrown to the response if the first value is null.
	"""
	if (var[1] and var[0] is None):
		return handle_invalid_parameter("invalid_value", var[1])

	message = MSG[message_id].copy()
	message["message"] = message["message"].format(*format)
	return json_response(message, status)

def get_list_id(collection, index = "id", ignore_filter = False):
	"""Lists the indexes/keys of a collection."""
	if (not ignore_filter):
		collection = [register[index] for register in list(collection)]
	return "'" + ("', '".join(collection)) + "'"