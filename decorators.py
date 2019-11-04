import database as db
import time
from functools import wraps
from flask import request
from meta import CACHE, ENV, MSG
from utils import HttpStatus, json_response

def check_maintenance(module, service):
	"""Forces a maintenance chance for the specific service."""
	def decorator(f):
		@wraps(f)
		def wrapper(self):
			if (db.in_maintenance(module, service)):
				return json_response(MSG["maintenance"], HttpStatus.SERVICE_UNAVAILABLE)

			return f(self)
		return wrapper
	return decorator

def require_access_token(f):
	"""Forces the request to send an authorization token to access a specific service."""
	@wraps(f)
	def wrapper(self):
		# Token
		if (db.count(db.access_token, { "token": request.headers.get("authorization") }) == 0):
			return json_response(MSG["unauthorized"], HttpStatus.UNAUTHORIZED)

		return f(self)
	return wrapper

def get_request_name(request):
	"""Generates a unique and temporary request name to save as cache index."""
	return '\001'.join(request.args) + '\002' + '\001'.join(request.args.values())

def cache(f_name):
	"""Caches any response submitted by the service."""
	def decorator(f):
		@wraps(f)
		def wrapper(self):
			if (f_name not in CACHE):
				CACHE[f_name] = { }

			request_name = get_request_name(request)

			current_time = time.time()
			if (request_name in CACHE[f_name] and CACHE[f_name][request_name]["time"] > current_time):
				return CACHE[f_name][request_name]["content"]

			CACHE[f_name][request_name] = {
				"time": current_time + ENV["api"]["cache_time"],
				"content": None
			}

			response = f(self)
			CACHE[f_name][request_name]["content"] = response
			return response
		return wrapper
	return decorator

def remove_cache(src_f_name):
	"""Removes any cached response from a specific service once the current service (which is not the same) is called."""
	def decorator(f):
		@wraps(f)
		def wrapper(self):
			response = f(self)

			if (src_f_name in CACHE and (300 > int(response.status[0:3]) >= 200)): # Error messages are not deleted from the cache
				request_name = get_request_name(request)
				if (request_name in CACHE[src_f_name]):
					del CACHE[src_f_name][request_name]

			return response
		return wrapper
	return decorator

