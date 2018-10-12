from flask import Flask
webapp = Flask(__name__)

from app import Welcome
from app import SignIn
from app import SignUp
from app import HomePage
from app import LogOut
