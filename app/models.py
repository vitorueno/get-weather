from app import db, api_clima
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class UsuarioModel(db.Model, UserMixin):
    cpf_usuario = db.Column(db.String(14), primary_key=True, nullable=False)
    nome_completo = db.Column(db.String, nullable=False)
    nome_usuario = db.Column(db.String(20), nullable=False, unique=True)
    caminho_foto = db.Column(db.String, nullable=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    email_confirmado = db.Column(db.Boolean)
    senha_hash = db.Column(db.String(256))
    lista_cidades = db.relationship('CidadeModel', back_populates='usuario')

    def __init__(self, cpf, nome_completo, nome_usuario, email, senha, caminho_foto):
        self.cpf_usuario = cpf
        self.nome_completo = nome_completo
        self.nome_usuario = nome_usuario
        self.email = email
        self.set_senha_hash(senha)
        self.caminho_foto = caminho_foto

    def get_id(self):
        return self.cpf_usuario

    def set_senha_hash(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class CidadeModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    nome_cidade = db.Column(db.String, nullable=False)
    usuario = db.relationship('UsuarioModel', back_populates='lista_cidades')
    cpf_usuario = db.Column(db.String(20), db.ForeignKey(
        'usuario_model.cpf_usuario'), nullable=False)
    favorito = db.Column(db.Boolean, nullable=False)
    notificavel = db.Column(db.Boolean, nullable=False)
    descricao = db.Column(db.String)

    def __init__(self, id, nome, cpf, favorito, notificavel, descricao):
        self.nome_cidade = nome
        self.id = id
        self.cpf_usuario = cpf
        self.favorito = favorito
        self.notificavel = notificavel
        self.descricao = descricao


class AvaliacaoSiteModel(db.Model):
    nome_usuario = db.Column(db.String(20), db.ForeignKey(
        'usuario_model.nome_usuario'), nullable=False)
    caminho_foto = db.Column(db.String, db.ForeignKey(
        'usuario_model.caminho_foto'), nullable=True)
    cpf_usuario = db.Column(db.String(20), db.ForeignKey(
        'usuario_model.cpf_usuario'), nullable=False, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    data = db.Column(db.DATE, nullable=False)
    comentario = db.Column(db.String)

    def __init__(self, nome_usuario, cpf_usuario, nota, data, comentario, caminho_foto):
        self.nome_usuario = nome_usuario
        self.cpf_usuario = cpf_usuario
        self.nota = nota
        self.data = data
        self.comentario = comentario
        self.caminho_foto = caminho_foto
