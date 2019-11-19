import random
import os
from uuid import uuid4
import tzlocal
import pytz
import datetime
from pyowm.exceptions.api_response_error import NotFoundError
from app import app, db,login_manager,api_clima
from flask import render_template, redirect,request, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug import secure_filename
from app.models import UsuarioModel, CidadeModel, AvaliacaoSiteModel, CidadeDoJson
from app.forms import (CadastroUsuarioForm,LoginUsuarioForm,CadastroCidadeForm,
    EdicaoCidadeForm, AvaliacaoSiteForm,EdicaoUsuarioForm,AlterarSenhaForm, 
    PesquisarCidadeForm)

import json


#página inicial + tela  de login + cadastro de usuário
@app.route('/',methods=['get','post'])
@app.route('/home',methods=['get','post'])
def carregar_index():
    #avaliação do site
    avaliacoes = AvaliacaoSiteModel.query.all()
    notas = []
    comentarios = []
    for avaliacao in avaliacoes:
        notas.append(avaliacao.nota)
        comentarios.append(avaliacao.comentario)
    media = calcular_media_notas(notas)

    #Conteúdo da página inicial
    cidades=['Berlin','Tokyo','New York','Washington','Brasilia','Moscow']
    climas = []
    for cidade in cidades:
        objeto_clima = coletar_objetos_climaticos(cidade)[0]
        clima_atual = objeto_clima.get_weather()
        climas.append(clima_atual)

    return render_template('index.html',climas=climas,media=media,comentarios=comentarios,avaliacoes=avaliacoes)

#cadastrar usuário isolado
@app.route('/cadastrar_usuario',methods=['get','post'])
def cadastrar_usuario():
    form_cad_user = CadastroUsuarioForm()

    erros = []
    if form_cad_user.validate_on_submit():
        
        #padronizar formato do cpf(sem ponto e traço)
        form_cad_user.cpf.data = padronizar_cpf(form_cad_user.cpf.data)

        #clausulas dos futuros ifs de verificação (conteúdos únicos no BD e validação de cpf)
        cpf_ja_cadastrado = UsuarioModel.query.filter_by(cpf_usuario=form_cad_user.cpf.data).first()
        usuario_ja_cadastrado = UsuarioModel.query.filter_by(nome_usuario=form_cad_user.nome_usuario.data).first()
        cpf_valido = validar_cpf(form_cad_user.cpf.data)
        email_ja_cadastrado = UsuarioModel.query.filter_by(email=form_cad_user.email.data).first()

        #inicio das verificações
        if not cpf_ja_cadastrado: #verifica se o cpf já não está cadastrado (erro chave 1ª)
            if cpf_valido: #verifica se o cpf é válido (regras gorverno)
                if not usuario_ja_cadastrado: #verifica se o nome de usuário ja foi usado
                    if not email_ja_cadastrado:
                        if form_cad_user.imagem.data.filename != "": 
                            nome_arquivo = secure_filename(form_cad_user.imagem.data.filename)
                            form_cad_user.imagem.data.save(os.path.join(app.config['UPLOAD_FOLDER'],nome_arquivo))
                            novo_usuario = UsuarioModel(form_cad_user.cpf.data,form_cad_user.nome_completo.data,
                                form_cad_user.nome_usuario.data,form_cad_user.email.data,form_cad_user.senha.data,
                                "img/"+nome_arquivo)
                        else:
                            novo_usuario = UsuarioModel(form_cad_user.cpf.data,form_cad_user.nome_completo.data,
                                form_cad_user.nome_usuario.data,form_cad_user.email.data,form_cad_user.senha.data,
                                "img/"+'ovo.jpg')
                        db.session.add(novo_usuario)
                        db.session.commit()
                        return redirect('/home')
                    else:
                        #email ja foi usado, mostrará um erro
                        erros.append('Email já cadastrado. Por favor tente outro')
                else:
                    #nome de usuário ja foi usado, mostrará um erro
                   erros.append('Nome de usuário já cadastrado. Por favor tente outro')
            else:
                #cpf já foi usado, logo mostrará um erro
                erros.append('CPF inválido. Por favor, informe outro.') 
        else:
            #se cpf já estiver cadastrado
            erros.append('CPF já cadastrado. Por favor, tente outro.') 
            
    return render_template('cadastro_user.html',form=form_cad_user,erros=erros)

#editar usuário
@app.route('/editar_usuario',methods=['get','post'])
@login_required
def editar_usuario():
    form_edit_user = EdicaoUsuarioForm()
    erros = []
    #simplificando nomes
    usuario = form_edit_user.nome_usuario
    nome = form_edit_user.nome_completo
    email = form_edit_user.email
    imagem = form_edit_user.imagem
    
    usuario.render_kw = {"value": current_user.nome_usuario}
    nome.render_kw = {"value": current_user.nome_completo}
    email.render_kw = {"value": current_user.email}

    if form_edit_user.validate_on_submit():
        if imagem.data.filename != "":
            nome_arquivo = secure_filename(imagem.data.filename)
            arquivo_atual = os.path.split(current_user.caminho_foto)[1]
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],arquivo_atual))
            imagem.data.save(os.path.join(app.config['UPLOAD_FOLDER'],nome_arquivo))
            current_user.caminho_foto = "img/" + nome_arquivo
        
        if  usuario.data != current_user.nome_usuario:
            usuario_existente = UsuarioModel.query.filter_by(nome_usuario=usuario.data).first()
        else:
            usuario_existente = None
            
        if  email.data != current_user.email:
            email_existente = UsuarioModel.query.filter_by(email=email.data).first()
        else:
            email_existente = None
        
        if usuario_existente is None:
            if email_existente is None:
                current_user.nome_completo = nome.data
                current_user.usuario = usuario.data
                current_user.email = email.data
                db.session.merge(current_user)
                db.session.commit()
                return redirect('/perfil')
            else:
                erros.append("Email já em uso. Tente outro, por favor.")
        else:
            erros.append("Nome de usuário já em uso. Tente outro, por favor.")

    
    return render_template('editar_usuario.html',form=form_edit_user,erros=erros)

@app.route('/alterar_senha',methods=['get','post'])
@login_required
def alterar_senha():
    form = AlterarSenhaForm()
    erros = []
    if form.validate_on_submit():
        if current_user.checar_senha(form.senha_atual.data):
            current_user.set_senha_hash(form.nova_senha.data)
            db.session.merge(current_user)
            db.session.commit()
            return redirect('/perfil')
        else:
            erros.append('Senha incorreta, por favor tente novamente.')
        
    return render_template('alterar_senha.html',form=form,erros=erros)

#logar
@app.route('/logar_usuario',methods=['get','post'])
def logar_usuario():
    erros = []
    form_login = LoginUsuarioForm()
    if form_login.validate_on_submit():
        usuario = UsuarioModel.query.filter_by(nome_usuario=form_login.nome_usuario.data).first()
        if usuario is not None:
            verificacao_senha = usuario.checar_senha(form_login.senha.data)
            if verificacao_senha:
                login_user(usuario)
                return redirect('/home')
            else:
                erros.append('Usuário e/ou senha inválido. Por favor, digite outro.')
        else:
            erros.append('Usuário e/ou senha inválido. Por favor, digite outro.')
    return render_template('login_user.html',form=form_login,erros=erros)

#logout usuário
@app.route('/deslogar_usuario',methods=['get','post'])
@login_required
def deslogar_usuario():
    logout_user()
    return redirect('/home')

#cadastrar cidade
@app.route('/cadastrar_cidade',methods=['get','post'])
@login_required
def cadastrar_cidade():
    form_cad_city = CadastroCidadeForm()
    cidades_possiveis = CidadeDoJson.query.all()
    
    if form_cad_city.validate_on_submit():
        
        while True:
            id_gerado = uuid4()
            busca_por_id_repetido = CidadeModel.query.filter_by(id=str(id_gerado)).first()
            if busca_por_id_repetido is None:
                break

        cidade_valida = coletar_objetos_climaticos(form_cad_city.nome_cidade.data)

        if cidade_valida is not None: #cidade válida
    
            cidade_ja_cadastrada = CidadeModel.query.filter_by(nome_cidade=form_cad_city.nome_cidade.data,
                                                               cpf_usuario=current_user.cpf_usuario).first()
            if cidade_ja_cadastrada is not None:
                msg_ja_cad = 'Cidade já cadastrada, Por favor tente outro nome.' 
                list(form_cad_city.nome_cidade.errors).append(msg_ja_cad)
                
            else:
                nova_cidade =  CidadeModel(str(id_gerado),form_cad_city.nome_cidade.data,
                    current_user.cpf_usuario,form_cad_city.favorita.data,form_cad_city.notificacao.data,
                    form_cad_city.descricao_cidade.data)
                current_user.lista_cidades.append(nova_cidade)
                db.session.merge(current_user)
                db.session.add(nova_cidade)
                db.session.commit()
                return redirect('/lista_cidades')
            
        else: #cidade não válida
            nome_cidade = form_cad_city.nome_cidade.data
            msg_erro_cidade = f'{nome_cidade} não é um nome de cidade válido para a API de clima. Por favor tente outro.' 
            list(form_cad_city.nome_cidade.errors).append(msg_erro_cidade)
            
    return render_template('cadastro_city.html',form=form_cad_city,lista_cidades=cidades_possiveis)


#lista de cidades
@app.route('/lista_cidades',methods=['get','post'])
@login_required
def listar_cidades():
    '''
    itens_request = request.args
    favorito = itens_request.getlist('favorito')
    notificavel = itens_request.getlist('notificavel')
    string_pesquisa = itens_request.getlist('pesquisa')
    print(favorito)
    print(notificavel)
    print(string_pesquisa)
    '''
    form = PesquisarCidadeForm()
    cidades = []
    if form.validate_on_submit():
        for cidade in current_user.lista_cidades:
            if form.nome_cidade.data.capitalize() in cidade.nome_cidade.capitalize():
                cidades.append(cidade)
    else:
        cidades = current_user.lista_cidades
    return render_template('Lista_cidade.html',cidades=cidades,form=form)


@app.route('/lista_cidades/favoritas',methods=['get','post'])
@login_required
def listar_cidades_favoritas():
    form = PesquisarCidadeForm()
    cidades = []
    if form.validate_on_submit():
        for cidade in current_user.lista_cidades:
            if form.nome_cidade.data.capitalize() in cidade.nome_cidade.capitalize():
                cidades.append(cidade)
    else:
        for cidade in current_user.lista_cidades:
            if cidade.favorito:
                cidades.append(cidade)
    return render_template('Lista_cidade.html',cidades=cidades,form=form)


@app.route('/lista_cidades/notificavel',methods=['get','post'])
@login_required
def listar_cidades_notificavel():
    form = PesquisarCidadeForm()
    cidades = []
    if form.validate_on_submit():
        for cidade in current_user.lista_cidades:
            if form.nome_cidade.data.capitalize() in cidade.nome_cidade.capitalize():
                cidades.append(cidade)
    else:
        for cidade in current_user.lista_cidades:
            if cidade.notificavel:
                cidades.append(cidade)
    return render_template('Lista_cidade.html',cidades=cidades,form=form)
    
#deletar cidade
@app.route('/deletar_cidade/<string:id>',methods=['get','post'])
@login_required
def deletar_cidade(id):
    cidade = CidadeModel.query.get_or_404(id)
    if cidade is not None:
        db.session.delete(cidade)
        db.session.commit()
        return redirect('/lista_cidades') 

#editar cidade
@app.route('/editar_cidade/<string:id>',methods=['get','post'])
@login_required
def editar_cidade(id):
    cidade = CidadeModel.query.get_or_404(id)
    form_edicao_city = EdicaoCidadeForm()
    form_edicao_city.descricao_cidade.render_kw = {"placeholder": cidade.descricao}
    if cidade.notificavel:
        form_edicao_city.notificacao.render_kw = {"checked":"checked"}
    if cidade.favorito:
        form_edicao_city.favorita.render_kw = {"checked":"checked"}

    if form_edicao_city.validate_on_submit():
        #condições
        descr_diferente = form_edicao_city.descricao_cidade.data != cidade.descricao
        fav_diferente = form_edicao_city.favorita != cidade.favorito
        notific_diferente = form_edicao_city.notificacao.data != cidade.notificavel
        if cidade.descricao is not None and descr_diferente:
            cidade.descricao = form_edicao_city.descricao_cidade.data
        if cidade.favorito is not None and fav_diferente:
            cidade.favorito = form_edicao_city.favorita.data
        if cidade.notificavel is not None and notific_diferente:
            cidade.notificavel = form_edicao_city.notificacao.data

        db.session.merge(cidade)
        db.session.commit()
        return redirect('/lista_cidades') 
    return render_template('editar_city.html',form=form_edicao_city,cidade=cidade)

#informações da cidade
@app.route('/cidade/<string:id>',methods=['get','post'])
@login_required
def exibir_cidade(id):
    cidade = CidadeModel.query.get_or_404(id)
    #carrega os objetos de observação
    objeto_cidade,objeto_previsao = coletar_objetos_climaticos(cidade.nome_cidade)
    #coleta o clima atual da cidade
    clima_agora = objeto_cidade.get_weather()
    #coleta as previsões do objeto de previsão
    previsoes = objeto_previsao.get_forecast()
    #coleta o clima de cada uma dessas previsões
    previsoes_clima = previsoes.get_weathers()
    fuso_horario = tzlocal.get_localzone()
    return render_template('city_weather.html',cidade=cidade,clima=clima_agora,
        previsoes=previsoes_clima, fuso = fuso_horario)

#formulário de avaliação
@app.route('/avaliacao_form',methods=['get','post'])
@login_required
def avaliar_site():
    ja_avaliado = AvaliacaoSiteModel.query.filter_by(cpf_usuario=current_user.cpf_usuario).first()
    form_avaliacao = AvaliacaoSiteForm()
    if form_avaliacao.validate_on_submit():
        if ja_avaliado:
            db.session.delete(ja_avaliado)
            db.session.commit()

        nova_avaliacao = AvaliacaoSiteModel(current_user.nome_usuario,current_user.cpf_usuario,form_avaliacao.nota.data,
            datetime.datetime.now(tz=pytz.utc),form_avaliacao.comentario.data,current_user.caminho_foto)
        db.session.add(nova_avaliacao)
        db.session.commit()
        return redirect('/home')
    return render_template('avaliacao.html',form=form_avaliacao)


@login_manager.user_loader
def load_user(cpf_usuario):
    return UsuarioModel.query.filter_by(cpf_usuario=cpf_usuario).first()

@app.route('/excluir_conta',methods=['get','post'])
@login_required
def excluir_conta():
    for cidade in current_user.lista_cidades:
        db.session.delete(cidade)
    arquivo_atual = os.path.split(current_user.caminho_foto)[1]
    if arquivo_atual != "img/"+"ovo.jpg":
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],arquivo_atual))
    db.session.delete(current_user)
    db.session.commit()
    return redirect('/home')


#perfil
@app.route('/perfil',methods=['get','post'])
@login_required
def carregar_perfil():
    return render_template('perfil.html',foto=current_user.caminho_foto)

#404
@app.errorhandler(404)
def page_not_found(e):
    #flash("Erro 404: A página solicitada não foi implementada. Desculpe pelo inconveniente.")
    return render_template("erro404.html")

def verificar_existencia_cidade(nome_cidade:str):
    cidade_existente = CidadeDoJson.query.filter_by(name=nome_cidade).first() 
    return cidade_existente 

def coletar_objetos_climaticos(nome_cidade:str):
    cidade = verificar_existencia_cidade(nome_cidade)
    if cidade is not None:
        objeto_cidade = api_clima.weather_at_place(nome_cidade.capitalize())
        objeto_previsao = api_clima.three_hours_forecast(nome_cidade.capitalize())
        return objeto_cidade,objeto_previsao
    else:
        return None


def calcular_media_notas(lista_notas:list):
    tamanho_lista = len(lista_notas)
    if tamanho_lista > 0:
        soma_notas = sum(lista_notas)
        media = soma_notas/tamanho_lista
        return media
    return None

def padronizar_cpf(cpf):
    if type(cpf) == int:
        cpf = str(cpf)

    cpf = cpf.strip()

    if "-" in cpf:
        cpf = cpf.replace("-","")
    
    if "." in cpf:
        cpf = cpf.replace(".","")

    return cpf

def validar_cpf(cpf):
    try:
        padronizar_cpf(cpf)

        #segmenta o cpf em duas partes
        cpf_sem_verific = cpf[:9]
        digitos_ver = cpf[9:]

        #geração do suposto primeiro digito verificador 
        soma1 = 0
        contagem1 = 10
        for numero in cpf_sem_verific:
            soma1 += int(numero) * contagem1
            contagem1 -= 1

        resto_soma1 = soma1%11
        if resto_soma1 < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto_soma1
        
        digito1 = str(digito1)
        segundo_passo = cpf_sem_verific + digito1

        soma2 = 0
        contagem2 = 11
        for numero in segundo_passo:
            soma2 += int(numero) * contagem2
            contagem2 -= 1
        
        resto_soma2 = soma2%11
        if resto_soma2 < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto_soma2
        
        digito2 = str(digito2)
        
        if digito1 == digitos_ver[0] and digito2 == digitos_ver[1]:
            return True
        return False
    except:
        return False
