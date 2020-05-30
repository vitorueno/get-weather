from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, IntegerField, BooleanField,
     SubmitField,TextAreaField,FloatField,FileField,SelectField)
from wtforms.validators import InputRequired, Length, EqualTo, Email,NumberRange
# from email_validator import validate_email 
from flask_uploads import UploadSet, IMAGES
from flask_wtf.file import FileAllowed
from app import Config

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

DESCRICAO = {
    "nome_completo": "Ex: José da Silva",
    "nome_usuario":"Ex: explosaogameplays. Entre 1 a 20 caracteres",
    "cpf":"O cpf deve ser válido, ter entre 11 a 14 caracteres, com ou sem pontos",
    "email":"Use um e-mail válido para utilizar todos os recursos do site",
    "senha": "Entre 3 a 32 caracteres",
    "confirm_senha": "Deve ser igual a senha digitada",
    "foto":"Foto de perfil png, jpg ou jpeg. Selecione nenhuma para utilizar a padrão",
    "nome_cidade":"Use nomes internacionais para cidades estrangeiras",
    "desc_cidade":"Ex: Já visitei.",
    "notificacao": "cidades notificáveis enviarão e-mails para vocês com o clima atual dela",
    "nota":"ex: 9",
    "comentario":"ex: Muito bom esse site!",
}   


class CadastroUsuarioForm(FlaskForm):
    nome_completo = StringField("Nome completo:", description=DESCRICAO["nome_completo"],
                    validators=[InputRequired(message=ERROS['requerido'])])

    nome_usuario = StringField("Nome de usuário:",validators=[Length(min=1,max=20,message=ERROS['quant_caracter_usuario']),
                        InputRequired(message=ERROS['requerido'])], description=DESCRICAO["nome_usuario"])

    cpf = StringField("CPF:", validators=[InputRequired(message=ERROS['requerido']),
                Length(min=11,max=14,message=ERROS['tamanho_cpf'])],description=DESCRICAO["cpf"])

    email = StringField("Email:", description=DESCRICAO["email"],validators=[Email(message=ERROS['email']),
                Length(min=10,max=256,message=ERROS['tamanho_email']),InputRequired(message=ERROS['requerido']) ])

    senha = PasswordField("Senha:", description=DESCRICAO["senha"],validators=[InputRequired(message=ERROS['requerido']),
                Length(min=3,max=32,message=ERROS['tamanho_senha'])])

    confirmacao_senha = PasswordField("Digite a Senha novamente: ", description=DESCRICAO["confirm_senha"],
                            validators=[InputRequired(message=ERROS['requerido']),Length(min=3,max=32,message=ERROS['tamanho_senha']),
                            EqualTo('senha',message=ERROS['senhas_iguais'])])
    
    imagem = FileField('Foto de Perfil:', description=DESCRICAO['foto'] ,validators=[FileAllowed(['jpg', 'png','jpeg'],
                message=ERROS['arquivo_foto']) ])
    
    enviar = SubmitField("Enviar")


class LoginUsuarioForm(FlaskForm):
    nome_usuario = StringField("Nome de usuário", description=DESCRICAO["nome_usuario"], validators=[InputRequired(message=ERROS['requerido']), 
                                    Length(min=1,max=20,message=ERROS['quant_caracter_usuario']) ])
    
    senha = PasswordField("Senha", description=DESCRICAO["senha"],validators=[InputRequired(message=ERROS['requerido']),
                Length(min=3,max=32,message=ERROS['tamanho_senha'])])
    
    lembreme = BooleanField("Lembre-me")
    
    logar = SubmitField("Logar")


class CadastroCidadeForm(FlaskForm):
    nome_cidade = StringField("Nome da cidade", description=DESCRICAO['nome_cidade'],
                validators=[InputRequired(message=ERROS['requerido']),Length(max=100,message=ERROS['tamanho_cidade'])])
    
    descricao_cidade = TextAreaField("Descrição da cidade",description=DESCRICAO["desc_cidade"])
    
    favorita = BooleanField("Cidade favorita")
    
    notificacao = BooleanField("Notificações por e-mail", description=DESCRICAO["notificacao"])
    
    enviar = SubmitField("Enviar")


class EdicaoCidadeForm(FlaskForm):
    descricao_cidade = TextAreaField("Descrição da cidade",description=DESCRICAO["desc_cidade"])
    
    favorita = BooleanField("Cidade favorita")
    
    notificacao = BooleanField("Notificação por e-mail",description=DESCRICAO["notificacao"])
    
    editar = SubmitField("Editar")


class AvaliacaoSiteForm(FlaskForm):
    nota = FloatField("Nota de 0 a 10",validators=[InputRequired(message=ERROS['requerido']),
        NumberRange(min=0,max=10,message=ERROS['range_numeros'])],description=DESCRICAO["nota"])
    
    comentario = TextAreaField("Comentário sobre o site",description=DESCRICAO["comentario"])
    
    avaliar = SubmitField("Avaliar site")
    
    
class EdicaoUsuarioForm(FlaskForm):
    nome_completo = StringField("Nome completo", validators=[InputRequired(message=ERROS['requerido'])],
                        description=DESCRICAO['nome_completo'])

    nome_usuario = StringField("Nome de usuário", validators=[Length(min=1,max=20,message=ERROS['quant_caracter_usuario']),
        InputRequired(message=ERROS['requerido'])],description=DESCRICAO["nome_usuario"])

    email = StringField("Email", validators=[Email(message=ERROS['email']),Length(min=10,max=256,message=ERROS['tamanho_email']), 
        InputRequired(message=ERROS['requerido'])], description=DESCRICAO["email"])

    imagem = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png','jpeg'],message=ERROS['arquivo_foto'])],
            description=DESCRICAO['foto'])

    editar = SubmitField("Editar Perfil")
    
    
class AlterarSenhaForm(FlaskForm):
    senha_atual = PasswordField("Senha atual", validators=[InputRequired(message=ERROS['requerido']),
                                                     Length(min=3,max=32,message=ERROS['tamanho_senha'])])

    nova_senha = PasswordField("Nova Senha", validators=[InputRequired(message=ERROS['requerido']),
            Length(min=3,max=32,message=ERROS['tamanho_senha'])], description=DESCRICAO["senha"])
    
    confirm_nova_senha = PasswordField("Digite a Senha novamente", validators=[InputRequired(message=ERROS['requerido']),
            Length(min=3,max=32,message=ERROS['tamanho_senha']),EqualTo('nova_senha',message=ERROS['senhas_iguais'])],
            description=DESCRICAO["confirm_senha"])

    editar = SubmitField("Editar Senha")


class PesquisarCidadeForm(FlaskForm):
    nome_cidade= StringField("Pesquisar cidade por nome:", validators=[Length(max=100,message=ERROS['tamanho_cidade'])])

    pesquisar = SubmitField("Pesquisar cidade")
    
    
class RecuperarSenhaForm(FlaskForm):
    cpf_usuario = StringField("Informe seu CPF:", validators=[InputRequired(message=ERROS['requerido']),
                Length(min=11,max=14,message=ERROS['tamanho_cpf'])], description=DESCRICAO["cpf"])
    
    recuperar_senha = SubmitField("recuperar senha")
