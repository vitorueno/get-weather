from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pyowm import OWM
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
api_clima = OWM(Config.CHAVE_API_CLIMA,language='pt')
mail = Mail(app)

from app import routes
from app import models
from app import forms