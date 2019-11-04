from app import app
import database
from meta import ENV

if (__name__ == "__main__"):
	app.run(host = ENV["api"]["host"], port = ENV["api"]["port"])