# app/__init__.py

from flask import Flask, session
import os

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.secret_key = os.urandom(24)


# Load the views
from app import view
from app import modals

# Load the config file
app.config.from_object('config')