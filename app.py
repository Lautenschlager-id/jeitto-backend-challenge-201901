from flask import Flask
from flask_restful import Api
from phone.product import Product
from phone.recharge import Recharge

app = Flask(__name__)

api = Api(app)
api.add_resource(Product, "/phone/product")
api.add_resource(Recharge, "/phone/recharge")