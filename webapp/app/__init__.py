from flask import Flask
webapp = Flask(__name__)

webapp.config['UPLOAD_FOLDER'] = 'C:\\Users\\81466\\Desktop\\webapp\\upload_images'
webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'

from app import Welcome
from app import SignIn
from app import SignUp
from app import HomePage
from app import LogOut
from app import ImgDetail
from app import sql