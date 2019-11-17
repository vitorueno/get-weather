import json
from app.models import CidadeDoJson
from app import db
import datetime

class Cidade():
    def __init__(self, id, name, country, coord):
        self.name = name
        self.id = id
        self.country = country
        self.coord = coord

    def __repr__(self):
        return f'<Cidade {self.name}>'


lista_cidades = []
with open('city.list.min.json','r',encoding="utf8") as cidades_file:
    cidades_dados = json.loads(cidades_file.read())
    for cidade in cidades_dados:
        nova_cidade = CidadeDoJson(cidade['id'],cidade['name'],cidade['country'],cidade['coord'])
        try:
            db.session.add(nova_cidade)
            db.session.commit()
            print(datetime.datetime.now())
        except:
            print(f'FAIL {datetime.datetime.now()}')


