import os
import platform

class Config:
    SECRET_KEY = "segredo"
    SQLALCHEMY_DATABASE_URI = "sqlite:///clima.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CHAVE_API_CLIMA = 'e90b5f2bd0164471e6240f4fbaee3505'
    ERROS = {
        'requerido':'Campo obrigatório. Por favor, preencha.',
        'quant_caracter_usuario':'Quantidade de caracteres inválido. Por favor, tente outro nome de usuário.',
        'email':'Formato de e-mail inválido. Por favor, tente novamente.',
        'senhas_iguais':'A confirmação de senha deve ser igual a senha. Por favor tente novamente.',
        'range_numeros':'Você só pode dar uma nota entre 0 e 10. Por favor, tente outro número',
        'tamanho_senha':'A senha deve ter entre 3 e 32 caracteres. Por favor, informe outro valor',
        'tamanho_email':'O tamanho do E-mail deve estar entre 10 e 256 caracteres. Por favor tente novamente',
        'tamanho_cpf': 'O tamanho do cpf deve estar entre 11 e 14 caracteres. Por favor tente novamente',
        'tamanho_cidade': 'O nome da cidade deve ter no máximo 100 caracteres. Por favor tente novamente.',
        'arquivo_foto': 'A foto de perfil do usuário deve ter o formato de PNG ou JPG. Tente outra foto',
        'file_required': 'O arquivo é obrigatório. Por favor, coloque um.'
    }
    if platform.system() == "Windows":
        UPLOAD_FOLDER = "app\static\img"
    elif platform.system() == "Linux":
        UPLOAD_FOLDER = '/home/aluno/Downloads/get-weather/app/static/img'
