import os, base64
from flask import session, request
from werkzeug.security import generate_password_hash


class Abstract:
    """A parent class where session ids will be created"""
    def generate_id(self, session_key):
        """Method for generating unique session ids"""
        generated_id = os.urandom(10).hex()
        while generated_id in session[session_key]:
            generated_id = os.urandom(10).hex()
        return generated_id

class User(Abstract):
    """A class to define a store a user object"""
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.userid = self.generate_id('users')

class shoppinglist(Abstract):
    """A class to define and store a shoppinglist object"""
    def __init__(self, listname):
        self.listname = listname
        self.list_id = self.generate_id('shopping_list')
        self.userid = session['logged_in']['userid']

class item(shoppinglist):
	"""A class to define and store a items object"""
	def __init__(self, itemname, quantity, price, list_id):
		self.itemname =itemname
		self.quantity = quantity
		self.price = price
		self.list_id = list_id

		shoppinglist.list_id = list_id
		self.item_id = self.generate_id('items')
		self.userid = session['logged_in']['userid']