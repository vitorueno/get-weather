from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, IntegerField, BooleanField,
     SubmitField,TextAreaField,FloatField,FileField)
from wtforms.validators import InputRequired, Length, EqualTo, Email,NumberRange
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileRequired, FileAllowed


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

class CadastroUsuarioForm(FlaskForm):
    nome_completo = StringField("nome completo", validators=[InputRequired(message=ERROS['requerido'])])
    nome_usuario = StringField("nome de usuário", validators=[Length(min=1,max=20,message=ERROS['quant_caracter_usuario']),
        InputRequired(message=ERROS['requerido'])])
    senha = PasswordField("Senha", validators=[InputRequired(message=ERROS['requerido']),Length(min=3,max=32,message=ERROS['tamanho_senha'])])
    confirmacao_senha = PasswordField("Digite a Senha novamente", validators=[InputRequired(message=ERROS['requerido']),
        Length(min=3,max=32,message=ERROS['tamanho_senha']), EqualTo('senha',message=ERROS['senhas_iguais'])])
    email = StringField("email", validators=[Email(message=ERROS['email']),Length(min=10,max=256,message=ERROS['tamanho_email']),
        InputRequired(message=ERROS['requerido']) ])
    imagem = FileField('Foto de Perfil', validators=[FileRequired(message=['file_required']),FileAllowed(['jpg', 'png'],message=ERROS['arquivo_foto']) ])
    cpf = StringField("cpf", validators=[InputRequired(message=ERROS['requerido']),Length(min=11,max=14,message=ERROS['tamanho_cpf'])])
    enviar = SubmitField("enviar")

class LoginUsuarioForm(FlaskForm):
    nome_usuario = StringField("nome de usuário",validators=[InputRequired(message=ERROS['requerido']),
        Length(min=1,max=20,message=ERROS['quant_caracter_usuario']) ])
    senha = PasswordField("Senha",validators=[InputRequired(message=ERROS['requerido']), Length(min=3,max=32,message=ERROS['tamanho_senha'])])
    logar = SubmitField("logar")

class CadastroCidadeForm(FlaskForm):
    nome_cidade = StringField("nome da cidade", validators=[InputRequired(message=ERROS['requerido']), Length(max=100,message=ERROS['tamanho_cidade'])])
    descricao_cidade = TextAreaField("descrição da cidade")
    favorita = BooleanField("cidade favorita")
    notificacao = BooleanField("notificações por e-mail")
    enviar = SubmitField("enviar")

class EdicaoCidadeForm(FlaskForm):
    notificacao = BooleanField("notificação por e-mail")
    descricao_cidade = TextAreaField("descrição da cidade")
    favorita = BooleanField("cidade favorita")
    editar = SubmitField("editar")

class AvaliacaoSiteForm(FlaskForm):
    nota = FloatField("Nota de 0 a 10",validators=[InputRequired(message=ERROS['requerido']),
        NumberRange(min=0,max=10,message=ERROS['range_numeros'])])
    comentario = TextAreaField("Comentário sobre o site")
    avaliar = SubmitField("avaliar site")
    
