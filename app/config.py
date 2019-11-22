import os
import platform
from app.email_info import Email

class Config:
    SECRET_KEY = "segredo"
    SQLALCHEMY_DATABASE_URI = "sqlite:///clima.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHAVE_API_CLIMA = 'e90b5f2bd0164471e6240f4fbaee3505'
    if platform.system() == "Windows":
        UPLOAD_FOLDER = "app\static\img"
        
    #alterar o upload_folder para sua máquina linux
    elif platform.system() == "Linux":
        UPLOAD_FOLDER = '/home/aluno/Downloads/get-weather/app/static/img'
        
    config_email = Email()
    MAIL_USERNAME = config_email.EMAIL
    MAIL_PASSWORD = config_email.SENHA
    MAIL_SERVER = config_email.HOST
    MAIL_PORT = config_email.PORTA
    MAIL_DEFAULT_SENDER = config_email.EMAIL
    MAIL_USE_TLS = config_email.TLS 
    MAIL_USE_SSL = config_email.SSL
    