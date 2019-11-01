import os

class Config:
    SECRET_KEY = "segredo"
    SQLALCHEMY_DATABASE_URI = "sqlite:///clima.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHAVE_API_CLIMA = 'e90b5f2bd0164471e6240f4fbaee3505'
    UPLOAD_FOLDER = '/home/aluno/Downloads/get-weather/app/static/img'